import threading
import validators
from math import ceil
from config.config import NUM_OF_THREADS
from tqdm import tqdm
import time
from db.fetching_db import fetch_get_or_none_telemetry_log_live_server, fetch_get_or_none_live_server_match_data, \
    fetch_get_or_none_tournament_match_data, fetch_get_or_none_telemetry_log_tournament, \
    fetch_tournament_matches_by_tournament_id
from db.push_db import push_telemetry_log_event_server, push_telemetry_log_live_server, push_live_server_match_data, \
    push_tournament_match_data
from helper.my_logger import logger

from pubg_api_requests import get_tournament_match_info, get_match_info, get_tournament_matches, get_player_stats, \
    get_circles_from_match


def find_telemetry_url(data):
    for line in data:
        if 'attributes' in line and 'URL' in line['attributes']:
            return line['attributes']['URL']


def multithread_extract_circles_for_event_server(list_of_matches_and_telemetry, thread):
    with tqdm(total=len(list_of_matches_and_telemetry), desc=f"[{thread}] Extracting Circles Live Server...") as pbar:
        for match_telemetry in list_of_matches_and_telemetry:
            match_id = match_telemetry[0]
            telemetry_url = match_telemetry[1]

            already_in = fetch_get_or_none_telemetry_log_tournament(match_id)

            if already_in:
                continue

            circle_list = get_circles_from_match(telemetry_url)

            for entry in circle_list:
                game_state = entry['gameState']
                if game_state is None:
                    continue

                my_id = match_id + "." + str(entry['common']['isGame'])
                push_telemetry_log_event_server(_id=my_id,
                                                _elapsedTime=game_state['elapsedTime'],
                                                _numAliveTeams=game_state['numAliveTeams'],
                                                _numAlivePlayers=game_state['numAlivePlayers'],
                                                _poisonGasWarningPositionX=
                                                game_state['poisonGasWarningPosition'][
                                                    'x'],
                                                _poisonGasWarningPositionY=
                                                game_state['poisonGasWarningPosition'][
                                                    'y'],
                                                _poisonGasWarningRadius=game_state[
                                                    'poisonGasWarningRadius'],
                                                _isGame=entry['common']['isGame'],
                                                _matchId=match_id)
            pbar.update(1)


def multithread_extract_circles_for_live_server(list_of_matches_and_telemetry, thread):
    with tqdm(total=len(list_of_matches_and_telemetry), desc=f"[{thread}] Extracting Circles Live Server...") as pbar:
        for match_telemetry in list_of_matches_and_telemetry:
            match_id = match_telemetry[0]
            telemetry_url = match_telemetry[1]

            if fetch_get_or_none_telemetry_log_live_server(match_id):
                continue

            if not validators.url(telemetry_url):
                logger.warning(f"{telemetry_url} not valid!")
                continue

            circle_list = get_circles_from_match(telemetry_url)
            for entry in circle_list:
                game_state = entry['gameState']
                if game_state is None:
                    continue

                my_id = match_id + "." + str(entry['common']['isGame'])
                push_telemetry_log_live_server(_id=my_id,
                                               _elapsedTime=game_state['elapsedTime'],
                                               _numAliveTeams=game_state['numAliveTeams'],
                                               _numAlivePlayers=game_state['numAlivePlayers'],
                                               _poisonGasWarningPositionX=
                                               game_state['poisonGasWarningPosition'][
                                                   'x'],
                                               _poisonGasWarningPositionY=
                                               game_state['poisonGasWarningPosition'][
                                                   'y'],
                                               _poisonGasWarningRadius=game_state[
                                                   'poisonGasWarningRadius'],
                                               _isGame=entry['common']['isGame'],
                                               _matchId=match_id
                                               )
            pbar.update(1)


def split_list_into_n_parts(lst, n):
    if len(lst) == 0:
        return lst

    n = len(lst) if len(lst) < n else n
    size = ceil(len(lst) / n)
    return list(
        map(lambda x: lst[x * size:x * size + size],
            list(range(n)))
    )


def extract_circles_for_event_server(match_ids_and_telemetry_url):
    chunks = split_list_into_n_parts(match_ids_and_telemetry_url, NUM_OF_THREADS)

    threads = []
    for index, chunk in enumerate(chunks):
        if len(chunk) == 0:
            continue
        thread = threading.Thread(target=multithread_extract_circles_for_event_server, args=(chunk, f"Thread {index}"))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def extract_circles_for_live_server(match_ids_and_telemetry_url):
    chunks = split_list_into_n_parts(match_ids_and_telemetry_url, NUM_OF_THREADS)
    threads = []
    for index, chunk in enumerate(chunks):
        thread = threading.Thread(target=multithread_extract_circles_for_live_server, args=(chunk, f"Thread {index}"))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def get_url_match_id_from_match_response(match_info_response, match_id):
    if 'errors' in match_info_response:
        logger.warning(f"Match bugged: {match_id}!")
        return None, None, None

    match_data = match_info_response['data']
    if match_data is None:
        logger.warning(f"Match Data bugged: {match_id}!")

    match_data_attributes = match_data['attributes']
    if match_data_attributes is None:
        logger.warning(f"Match Data Attributes bugged: {match_id}!")

    match_include = match_info_response['included']
    if match_include is None:
        logger.warning(f"Match Data Includes bugged: {match_id}!")
    url = find_telemetry_url(match_include)

    if "squad-fpp" not in match_data_attributes['gameMode']:
        return None, None, None

    return url, match_data, match_data_attributes


def retrieve_matches_and_push_to_db_live(match_ids_to_fetch):
    match_id_and_telemetry_urls = list()
    for match_id in match_ids_to_fetch:
        if fetch_get_or_none_live_server_match_data(match_id) is not None:
            if fetch_get_or_none_telemetry_log_live_server(match_id) is not None:
                continue

        match_info_response = get_match_info(match_id)
        url, match_data, match_data_attributes = get_url_match_id_from_match_response(match_info_response, match_id)

        if url is None:
            continue

        match_id_and_telemetry_urls.append((match_id, url))
        push_live_server_match_data(_matchId=match_data['id'],
                                    _mapName=match_data_attributes['mapName'],
                                    _isCustomMatch=match_data_attributes['isCustomMatch'],
                                    _duration=match_data_attributes['duration'],
                                    _shardId=match_data_attributes['shardId'],
                                    _gameMode=match_data_attributes['gameMode'],
                                    _createdAt=match_data_attributes['createdAt'],
                                    _matchType=match_data_attributes['matchType'],
                                    _telemetryURL=url,
                                    )

    return match_id_and_telemetry_urls


def retrieve_matches_and_push_to_db_event(match_ids_to_fetch, tourney_ref):
    match_id_and_telemetry_urls = list()
    for match_id in match_ids_to_fetch:
        if fetch_get_or_none_tournament_match_data(match_id) is not None:
            if fetch_get_or_none_telemetry_log_tournament(match_id) is not None:
                continue

        match_info_response = get_tournament_match_info(match_id)

        url, match_data, match_data_attributes = get_url_match_id_from_match_response(match_info_response, match_id)

        if url is None:
            continue

        match_id_and_telemetry_urls.append((match_id, url))
        push_tournament_match_data(_matchId=match_data['id'],
                                   _mapName=match_data_attributes['mapName'],
                                   _isCustomMatch=match_data_attributes['isCustomMatch'],
                                   _duration=match_data_attributes['duration'],
                                   _shardId=match_data_attributes['shardId'],
                                   _gameMode=match_data_attributes['gameMode'],
                                   _createdAt=match_data_attributes['createdAt'],
                                   _matchType=match_data_attributes['matchType'],
                                   _telemetryURL=url,
                                   _tournamentId=tourney_ref
                                   )
    return match_id_and_telemetry_urls


def extract_matches_for_tournaments(tournaments_ids):
    total_list_of_matches_and_telemetry_urls = list()
    for tournament_id in tqdm(tournaments_ids, desc="Extracting Matches...", colour="green"):
        time.sleep(7)
        already_fetched_matches = fetch_tournament_matches_by_tournament_id(tournament_id)

        matches_response = get_tournament_matches(tournament_id)

        if 'errors' in matches_response:
            logger.warning(f"No matches for tournament: {tournament_id}")
            continue
        matches = matches_response['included']

        match_ids_to_fetch = []
        if len(matches) == len(already_fetched_matches):
            logger.debug(f"{tournament_id}: {len(matches)} matches")
            continue
        else:
            for match in matches:
                match_id = match['id']
                if match['id'] not in already_fetched_matches:
                    match_ids_to_fetch += match_id
                else:
                    logger.debug(f"already in {match_id}")
            if len(match_ids_to_fetch) > 0:
                match_id_and_telemetry_urls = retrieve_matches_and_push_to_db_event(match_ids_to_fetch, tournament_id)
                total_list_of_matches_and_telemetry_urls += match_id_and_telemetry_urls

    return total_list_of_matches_and_telemetry_urls


def extract_circles_for_players(players):
    time.sleep(7)
    response = get_player_stats(players)
    if 'errors' in response:
        print(response['errors'])
        return None

    if response['data'] is None:
        return None
    data_response = response['data']

    if data_response[0] is None:
        return None

    data_response = data_response[0]

    if data_response['relationships'] is None:
        return None
    data_response_relationships = data_response['relationships']

    if data_response_relationships['matches'] is None:
        return None
    data_response_relationships_matches = data_response_relationships['matches']

    if data_response_relationships_matches['data'] is None:
        return None

    matches = data_response_relationships_matches['data']
    if matches is None or len(matches) == 0:
        return None

    match_ids_to_fetch = [match['id'] for match in matches]

    return retrieve_matches_and_push_to_db_live(match_ids_to_fetch)


def extract_matches_and_circles_for_live_server(player_names):
    for player in tqdm(player_names, desc=f"Extracting Circles Matchers for Players...", colour="green"):
        match_ids_with_telemetry_data = extract_circles_for_players([player])
        if match_ids_with_telemetry_data is not None and len(match_ids_with_telemetry_data) > 0:
            extract_circles_for_live_server(match_ids_with_telemetry_data)
        else:
            logger.warning(f"Player: {player} does not exist!")
