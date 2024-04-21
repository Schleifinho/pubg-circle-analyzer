# region Imports
import json
import time
import requests
from io import BytesIO
from config.config import DOWNLOAD_SPEED
from helper.my_logger import logger

from config.pubg_api_config import HEADER_AUTH, HEADER_NO_AUTH, HEADER_TELEMETRY, \
    PREFIX_GET_TOURNAMENT_MATCH_INFO_URL, PREFIX_GET_TOURNAMENT_URL, PREFIX_GET_LIVE_MATCH_INFO_URL, \
    PREFIX_GET_PLAYER_STATS_URL


# endregion

def download_throttled(url, header):
    response = requests.get(url, stream=True, headers=header)
    buffer = BytesIO()
    data = None
    try:
        # Check if the request was successful
        if response.status_code == 200:
            # Iterate over the content of the response
            for chunk in response.iter_content(chunk_size=DOWNLOAD_SPEED):
                # Start measuring the time
                start_time = time.time()
                buffer.write(chunk)
                # Calculate the time taken to process the chunk
                time_taken = time.time() - start_time

                # Calculate the time to sleep to limit the download rate
                sleep_time = max(0, (len(chunk) / DOWNLOAD_SPEED) - time_taken)

                # Sleep to throttle the download rate
                time.sleep(sleep_time)
            downloaded_content = buffer.getvalue()
            # Decode the bytes to a string
            json_string = downloaded_content.decode('utf-8')

            # Parse the JSON string into a Python dictionary
            data = json.loads(json_string)
        else:
            logger.warning(f"{url} -> ")
            logger.warning(f"Error Code: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed: {url}")
        logger.error(f"{e}")
    finally:
        buffer.close()
    return data
# region Event Server Requests


def get_tournament_list():
    url = PREFIX_GET_TOURNAMENT_URL
    tourneys = download_throttled(url, HEADER_AUTH)
    return tourneys


def get_tournament_matches(t_id):
    url = PREFIX_GET_TOURNAMENT_URL + "/" + str(t_id)
    response = download_throttled(url, HEADER_AUTH)
    return [] if response is None else response


def get_tournament_match_info(match_id):
    url = PREFIX_GET_TOURNAMENT_MATCH_INFO_URL + match_id
    return download_throttled(url, HEADER_NO_AUTH)


# endregion

# region Live Server Requests
def get_match_info(match_id):
    url = PREFIX_GET_LIVE_MATCH_INFO_URL + match_id
    return download_throttled(url, HEADER_NO_AUTH)


def get_player_stats(players):
    url = PREFIX_GET_PLAYER_STATS_URL
    for player in players:
        url += player + ","

    url = url[:-1]
    return download_throttled(url, HEADER_AUTH)


# endregion

# region General Requests
def get_circles_from_match(telemetry_url):
    telemetry_data = download_throttled(telemetry_url, HEADER_TELEMETRY)
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
