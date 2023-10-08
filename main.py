# region Imports
import os
from config.config import MAPS, RESULTS_FOLDER
from db.db import Tournaments, TournamentMatchData, \
    LiveServerMatchData, TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer, mysqlDB
from scripts.extract_tournament_circles import get_tournaments_and_push_to_db, get_scrims_and_push_to_db, \
    start_extracting_esport_circles, start_extracting_live_circles
from scripts.generate_heat_map import create_heat_maps
from helper.my_arg_parser import create_parser
from helper.my_logger import logger
from scripts.predict_zones import start_predicting_circles


# endregion

# region Inits
def create_db_and_tables():
    # create_db()
    mysqlDB.create_tables([LiveServerMatchData, Tournaments, TournamentMatchData,
                           TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer])


def create_folder():
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)

    for mapi in MAPS:
        if not os.path.exists(f"{RESULTS_FOLDER}/both/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/both/" + mapi[1].lower())
        if not os.path.exists(f"{RESULTS_FOLDER}/live/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/live/" + mapi[1].lower())
        if not os.path.exists(f"{RESULTS_FOLDER}/esport/" + mapi[1].lower()):
            os.makedirs(f"{RESULTS_FOLDER}/esport/" + mapi[1].lower())


# endregion

# region Load Commands
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


def load_heatmaps(args):
    create_folder()
    if args.maps:
        maps = [entry for entry in MAPS if entry[1].lower() in args.maps]
    else:
        maps = MAPS
    create_heat_maps(args.server, maps, args.date)


def load_predict(args):
    use_map = [entry for entry in MAPS if entry[1].lower() in args.maps][0]
    print(use_map)
    start_predicting_circles(args.server, use_map, args.zone, args.date)


# endregion

# region Main
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
# endregion
