import logging
from api_key import API_KEY_HIDDEN

# region General
NUM_OF_THREADS = 4

GREEN = "\033[92m"
RESET = "\033[0m"
LOGGING_LEVEL = logging.DEBUG

DATE_DEFAULT = "01-01-2023"
DATE_FORMAT = "%d-%m-%Y"
# endregion

# region HEATMAP CONFIG

RESULTS_FOLDER = "./results"

# should be same index in pretty
maps = ["Kiki_Main", "DihorOtok_Main", "Desert_Main", "Baltic_Main", "Tiger_Main"]
maps_pretty = ["Deston", "Vikendi", "Miramar", "Erangel", "Taego"]

MAPS = list(zip(maps, maps_pretty))
# endregion
