# region Imports
import logger
import requests
from config.pubg_api_config import HEADER_AUTH, HEADER_NO_AUTH, HEADER_TELEMETRY, \
    PREFIX_GET_TOURNAMENT_MATCH_INFO_URL, PREFIX_GET_TOURNAMENT_URL, PREFIX_GET_LIVE_MATCH_INFO_URL, \
    PREFIX_GET_PLAYER_STATS_URL


# endregion

# region Event Server Requests
def get_tournament_list():
    url = PREFIX_GET_TOURNAMENT_URL
    r = requests.get(url, headers=HEADER_AUTH)
    tourneys = r.json()
    return tourneys


def get_tournament_matches(t_id):
    url = PREFIX_GET_TOURNAMENT_URL + "/" + str(t_id)
    response = requests.get(url, headers=HEADER_AUTH)
    if response is None:
        return []

    obj = response.json()
    return obj


def get_tournament_match_info(match_id):
    url = PREFIX_GET_TOURNAMENT_MATCH_INFO_URL + match_id
    r = requests.get(url, headers=HEADER_NO_AUTH)
    return r.json()


# endregion

# region Live Server Requests
def get_match_info(match_id):
    url = PREFIX_GET_LIVE_MATCH_INFO_URL + match_id
    r = requests.get(url, headers=HEADER_NO_AUTH)
    return r.json()


def get_player_stats(players):
    url = PREFIX_GET_PLAYER_STATS_URL
    for player in players:
        url += player + ","

    url = url[:-1]
    r = requests.get(url, headers=HEADER_AUTH)
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError as ex:
        return None


# endregion

# region General Requests
def get_circles_from_match(telemetry_url):
    telemetry_data = requests.get(telemetry_url, headers=HEADER_TELEMETRY).json()
    filtered_list = get_circle_log_from_telemetry_data(telemetry_data)
    return filtered_list


def get_circle_log_from_telemetry_data(telemetry_data):
    filtered = []
    seen = set()
    for line in telemetry_data:
        if line['_T'] == "LogGameStatePeriodic":
            if line['common']['isGame'] not in seen and isinstance(line['common']['isGame'], int):
                filtered.append(line)
                seen.add(line['common']['isGame'])

    return filtered
# endregion
