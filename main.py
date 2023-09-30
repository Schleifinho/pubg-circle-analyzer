import os
import time
from datetime import datetime
from config.config import MAPS, DATE_FORMAT, RESULTS_FOLDER
from db.db import Tournaments, TournamentMatchData, \
    LiveServerMatchData, TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer, mysqlDB
from db.fetching_db import fetch_tournament_by_date
from db.push_db import push_tournament_list, push_tournament
from scripts.extract_tournament_circles import extract_matches_for_tournaments, extract_circles_for_event_server, \
    retrieve_matches_and_push_to_db_event, extract_matches_and_circles_for_live_server
from scripts.generate_heat_map import create_heat_maps
from helper.my_arg_parser import create_parser
from helper.my_logger import logger
from scripts.predict_zones import predict_svm
from scripts.pubg_api_requests import get_tournament_matches, get_tournament_list


def create_db_and_tables():
    # create_db()
    mysqlDB.create_tables([LiveServerMatchData, Tournaments, TournamentMatchData,
                           TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer])


def get_tournaments_and_push_to_db():
    tournaments = get_tournament_list()
    if tournaments['data'] and len(tournaments) > 0:
        push_tournament_list(tournaments['data'])
    else:
        print("Tournament List Invalid!")


def get_scrims_and_push_to_db(date_string):
    date = datetime.strptime(date_string, DATE_FORMAT)
    tourneys = fetch_tournament_by_date(date)
    total_list_of_matches_and_telemetry_urls = list()

    for tourney in tourneys:
        if str(tourney.id).count("-") > 0:
            clean_tourney = str(tourney.id).split("-")
            scrim_tourney = "test-" + clean_tourney[1]
            matches_response = get_tournament_matches(scrim_tourney)

            if "included" in matches_response:

                push_tournament(_id=scrim_tourney, _type="scrim", _createdAt=tourney.createdAt)

                if 'errors' in matches_response['data']:
                    print("No matches for tourney " + tourney.id)
                    continue
                matches = matches_response['included']

                match_id_and_telemetry_urls = retrieve_matches_and_push_to_db_event(matches, scrim_tourney)
                total_list_of_matches_and_telemetry_urls += match_id_and_telemetry_urls

        time.sleep(7)
    extract_circles_for_event_server(total_list_of_matches_and_telemetry_urls)


def create_folder():
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    for mapi in MAPS:
        if not os.path.exists(f"{RESULTS_FOLDER}/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/" + mapi[1].lower())

        if not os.path.exists(f"{RESULTS_FOLDER}/both/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/both/" + mapi[1].lower())
        if not os.path.exists(f"{RESULTS_FOLDER}/live/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/live/" + mapi[1].lower())
        if not os.path.exists(f"{RESULTS_FOLDER}/esport/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/esport/" + mapi[1].lower())


def load_init():
    create_db_and_tables()
    create_folder()


def load_tournaments(args):
    get_tournaments_and_push_to_db()
    get_scrims_and_push_to_db(args.date)


def load_extract(args):
    if args.server == "esport":
        logger.debug("Extracting for Esport Server...")
        start_extracting_esport_circles(args.tournament_ids, args.date)
    elif args.server == "live":
        logger.debug("Extracting for Live Server...")
        start_extracting_live_circles(args.player_list)
    elif args.server == "both":
        logger.debug("Extracting for Both Servers...")
        start_extracting_esport_circles(args.tournament_ids, args.date)
        start_extracting_live_circles(args.player_list)
    else:
        logger.error(f"Server option {args.server} unavailable!")


def start_extracting_live_circles(player_list):
    extract_matches_and_circles_for_live_server(player_list)


def start_extracting_esport_circles(tournament_ids, date_string):
    if not tournament_ids:
        logger.debug(f"Load all tournaments since {date_string}")
        date_object = datetime.strptime(date_string, DATE_FORMAT)
        date_only = date_object.date()
        tournaments = Tournaments.select(Tournaments.id).where(Tournaments.createdAt > date_only)

    else:
        logger.debug(f"Load tournaments: {tournament_ids}")
        tournaments = Tournaments.select().where(Tournaments.id.in_(tournament_ids))

    if len(tournaments) > 0:
        logger.info(f"Extracting Circles And Matches For {len(tournaments)} Tournaments")
        extract_matches_for_tournaments(tournaments)
    else:
        logger.warning("No tournaments found!")


def load_heatmaps(args):
    create_folder()
    if args.maps:
        maps = [entry for entry in MAPS if entry[1].lower() in args.maps]
    else:
        maps = MAPS
    create_heat_maps(args.server, maps, args.date)


def load_predict(args):
    c_map = args.maps[0]
    predict_svm([], (4, 4), c_map)


def main():
    args = create_parser()
    mysqlDB.connect()

    if args.init:
        logger.info("Load Init")
        load_init()
    elif args.tournaments:
        logger.info("Load Tournaments")
        load_tournaments(args)
    elif args.extract:
        logger.info("Load Extract")
        load_extract(args)
    elif args.heatmaps:
        logger.info("Load Heatmaps")
        load_heatmaps(args)
    elif args.predict:
        logger.info("Load Predict")
        load_predict(args)

    mysqlDB.close()


if __name__ == "__main__":
    main()
