# region Imports
from datetime import datetime
import logging
# endregion

# region General
NUM_OF_THREADS = 8
WINDOW_SIZE = 1080

# Unlimited -> DOWNLOAD_SPEED_MULTIPLIER = 0
# currently 1mb/sec
DOWNLOAD_SPEED_MULTIPLIER = 8
# multiply by 1024 to get kb/sec instead of b/sec
DOWNLOAD_SPEED = DOWNLOAD_SPEED_MULTIPLIER * 1024 * 1024

DEFAULT_PLAYER_LIST_FILE = "playerlist.txt"

GREEN = "\033[92m"
RESET = "\033[0m"
LOGGING_LEVEL = logging.INFO

DATE_DEFAULT = "01-03-2024"
DUE_DATE_DEFAULT = datetime.today().strftime('%d-%m-%Y')
DATE_FORMAT = "%d-%m-%Y"
# endregion

# region HEATMAP CONFIG

RESULTS_FOLDER = "./results"
HEATMAPS_FOLDER = f"{RESULTS_FOLDER}/heatmaps"
HISTOGRAMS_FOLDER = f"{RESULTS_FOLDER}/histograms"
ASSETS_FOLDER = "./assets"

# should be same index in pretty
maps = ["Kiki_Main", "DihorOtok_Main", "Desert_Main", "Baltic_Main", "Tiger_Main", "Neon_Main"]
maps_pretty = ["Deston", "Vikendi", "Miramar", "Erangel", "Taego", "Rondo"]

MAPS = list(zip(maps, maps_pretty))
# endregion

# DO NOT TOUCH
PUBG_MAP_SIZE = 816000
CIRCLE_3_SIZE = 67000
CIRCLE_4_SIZE = 40000
CIRCLE_8_SIZE = 7700