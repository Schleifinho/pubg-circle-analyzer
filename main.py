# region Imports
import os

from config.config import MAPS, RESULTS_FOLDER, HISTOGRAMS_FOLDER, HEATMAPS_FOLDER
from db.db import Tournaments, TournamentMatchData, \
    LiveServerMatchData, TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer, mysqlDB
from scripts.extract_tournament_circles import get_tournaments_and_push_to_db, get_scrims_and_push_to_db, \
    start_extracting_esport_circles, start_extracting_live_circles
from scripts.generate_heat_map import create_heat_maps
from helper.my_arg_parser import create_parser
from helper.my_logger import logger
from scripts.generate_histogram import start_generating_histogram
from scripts.predict_zones import start_predicting_circles


# endregion

# region Inits
def create_db_and_tables():
    mysqlDB.create_tables([LiveServerMatchData, Tournaments, TournamentMatchData,
                           TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer])


def create_results_folder():
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)


def create_histograms_folder():
    create_results_folder()
    if not os.path.exists(HISTOGRAMS_FOLDER):
        os.makedirs(HISTOGRAMS_FOLDER)

    for mapi in MAPS:
        if not os.path.exists(f"{HISTOGRAMS_FOLDER}/both/" + mapi[1].lower()):
            os.makedirs(f"{HISTOGRAMS_FOLDER}/both/" + mapi[1].lower())
        if not os.path.exists(f"{HISTOGRAMS_FOLDER}/live/" + mapi[1].lower()):
            os.makedirs(f"{HISTOGRAMS_FOLDER}/live/" + mapi[1].lower())
        if not os.path.exists(f"{HISTOGRAMS_FOLDER}/esport/" + mapi[1].lower()):
            os.makedirs(f"{HISTOGRAMS_FOLDER}/esport/" + mapi[1].lower())


def create_heatmaps_folder():
    create_results_folder()
    if not os.path.exists(HEATMAPS_FOLDER):
        os.makedirs(HEATMAPS_FOLDER)

    for mapi in MAPS:
        if not os.path.exists(f"{HEATMAPS_FOLDER}/both/" + mapi[1].lower()):
            os.makedirs(f"{HEATMAPS_FOLDER}/both/" + mapi[1].lower())
        if not os.path.exists(f"{HEATMAPS_FOLDER}/live/" + mapi[1].lower()):
            os.makedirs(f"{HEATMAPS_FOLDER}/live/" + mapi[1].lower())
        if not os.path.exists(f"{HEATMAPS_FOLDER}/esport/" + mapi[1].lower()):
            os.makedirs(f"{HEATMAPS_FOLDER}/esport/" + mapi[1].lower())

# endregion


# region Load Commands
def load_init():
    create_db_and_tables()
    create_histograms_folder()
    create_heatmaps_folder()


def load_tournaments(args):
    if args.tournament_ids is None:
        get_tournaments_and_push_to_db()
        get_scrims_and_push_to_db(args.date)
    else:
        for t_id in args.t_ids:
            Tournaments.create(id=t_id, createdAt=args.date, type=args.t_type)


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


def load_heatmaps(args):
    create_heatmaps_folder()
    if args.maps:
        maps = [entry for entry in MAPS if entry[1].lower() in args.maps]
    else:
        maps = MAPS
    create_heat_maps(args.server, maps, args.date, args.due_date, args.zone, args.match_type)


def load_predict(args):
    use_map = [entry for entry in MAPS if entry[1].lower() in args.maps][0]
    logger.info(f"Predict Map: {use_map}")
    start_predicting_circles(args.server, use_map, args.zone, args.date, args.due_date, args.mode, args.match_type)


# endregion

# region Main

def load_histogram(args):
    create_histograms_folder()
    if args.maps:
        maps = [entry for entry in MAPS if entry[1].lower() in args.maps]
    else:
        maps = MAPS

    start_generating_histogram(args.server, maps, args.date, args.due_date, args.zone, args.match_type)


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
        logger.info("Create Heatmaps")
        load_heatmaps(args)
    elif args.predict:
        logger.info("Load Predict")
        load_predict(args)
    elif args.histogram:
        logger.info("Create Histogram")
        load_histogram(args)

    mysqlDB.close()


if __name__ == "__main__":
    main()
# endregion
