# region Imports
import logging
# endregion

# region General
NUM_OF_THREADS = 8

GREEN = "\033[92m"
RESET = "\033[0m"
LOGGING_LEVEL = logging.DEBUG

DATE_DEFAULT = "01-01-2023"
DATE_FORMAT = "%d-%m-%Y"
# endregion

# region HEATMAP CONFIG

RESULTS_FOLDER = "./results"
HISTOGRAMS_FOLDER = "./histograms"
ASSETS_FOLDER = "./assets"

# should be same index in pretty
maps = ["Kiki_Main", "DihorOtok_Main", "Desert_Main", "Baltic_Main", "Tiger_Main"]
maps_pretty = ["Deston", "Vikendi", "Miramar", "Erangel", "Taego"]

MAPS = list(zip(maps, maps_pretty))
# endregion

# region Predict
WINDOW_SIZE = 1080

# DO NOT TOUCH
PUBG_MAP_SIZE = 816000
CIRCLE_3_SIZE = 67000
CIRCLE_4_SIZE = 40000
# endregion
