# region PUBG API CONFIG
from config.api_key import API_KEY_HIDDEN

API_KEY = API_KEY_HIDDEN  # replace with your API KEY

HEADER_AUTH = {
    "Authorization": "Bearer " + API_KEY,
    "Accept": "application/vnd.api+json"
}

HEADER_NO_AUTH = {
    "Accept": "application/vnd.api+json"
}

HEADER_TELEMETRY = {
    "Accept": "application/vnd.api+json",
    "Accept-Encoding": "gzip"
}

PREFIX_GET_TOURNAMENT_URL = "https://api.pubg.com/tournaments"
PREFIX_GET_TOURNAMENT_MATCH_INFO_URL = "https://api.pubg.com/shards/tournament/matches/"
PREFIX_GET_LIVE_MATCH_INFO_URL = "https://api.pubg.com/shards/steam/matches/"
PREFIX_GET_PLAYER_STATS_URL = "https://api.pubg.com/shards/steam/players?filter[playerNames]="
# endregion