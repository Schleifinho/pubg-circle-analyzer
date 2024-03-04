# region Imports
import argparse

from config.config import GREEN, DATE_DEFAULT, RESET, DUE_DATE_DEFAULT
from helper.my_logger import logger


# endregion

# region Create Parser
def create_parser():
    # Define ANSI color codes
    parser = argparse.ArgumentParser(description="PUBG Heatmap Interface",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Create a mutually exclusive group for flags -a and -b
    mutually_exclusive_group = parser.add_mutually_exclusive_group(required=True)

    # Init DB
    mutually_exclusive_group.add_argument("-i", "--init",
                                          action="store_true",
                                          help=f"{GREEN}Initialize DB and Folders{RESET}")
    # Get tournaments and scrims
    mutually_exclusive_group.add_argument("-t", "--tournaments",
                                          action="store_true",
                                          help=f"{GREEN}Fetch Tournaments{RESET}")

    # Extract Circles
    mutually_exclusive_group.add_argument("-e", "--extract",
                                          action="store_true",
                                          help=f"{GREEN}Extract Circles{RESET}\n"
                                               f"Optional Flag: '-maps'")

    # Create Heatmaps
    mutually_exclusive_group.add_argument("-c", "--heatmaps",
                                          action="store_true",
                                          help=f"{GREEN}Create Heatmaps{RESET}\n"
                                               f"Optional flags: '-maps'")

    # Predict Zones
    mutually_exclusive_group.add_argument("-p", "--predict",
                                          action="store_true",
                                          help=f"{GREEN}Predict Circles{RESET}\n"
                                               f"Starting from Zone 3, predict Zone 4 (default) or 8")

    # Create Histogram Of Zones
    mutually_exclusive_group.add_argument("-hist", "--histogram",
                                          action="store_true",
                                          help=f"{GREEN}Create Histogram{RESET}\n"
                                               f"Create Histogram For Zone 4 (default) or 8")

    parser.add_argument(
        "-pl", "--player_list",
        nargs='+',  # Indicates that the flag accepts multiple arguments
        type=str,  # Specifies the type of the elements in the list
        help=f"{GREEN}List of Players to extract data from{RESET}\n"
             "This flag is REQUIRED for extracting live server data!"
    )

    parser.add_argument(
        "-t_ids", "--tournament_ids",
        nargs='+',  # Indicates that the flag accepts multiple arguments
        type=str,  # Specifies the type of the elements in the list
        help=f"{GREEN}List of Tournament IDs to extract data from{RESET}\n"
             "This flag is OPTIONAL for extracting event server data!\n"
             "Not setting this flag will use all available tournaments"
    )

    parser.add_argument(
        "-t_type", "--tournament_type",
        type=str,
        help=f"{GREEN}Type Of Tournament To Add{RESET}\n"
             f"FORMAT: dd-mm-yyyy\n"
             f"Not setting this flag uses the DEFAULT Date from the config",
        choices=["tournament", "scrim"],
        default="tournament"
    )

    # Define additional flags that are not mutually exclusive with -a and -b
    parser.add_argument("-server",
                        type=str,
                        help=f"{GREEN}Set Server Flag{RESET}\n"
                             "'both' is not available for extracting (-e)!",
                        choices=["esport", "live", "both"],
                        default="esport")
    parser.add_argument(
        "-maps", "--maps",
        nargs='+',  # Indicates that the flag accepts multiple arguments
        type=str,  # Specifies the type of the elements in the list
        help=f"{GREEN}List of Maps{RESET}\n"
             "Choose one or more Maps. Not setting this flag will use all maps!",
        choices=["vikendi", "miramar", "erangel", "deston", "taego"],
        default=["vikendi", "miramar", "erangel", "deston", "taego"]
    )

    parser.add_argument(
        "-date",
        type=str,
        help=f"{GREEN}Data starting from this Date will be used{RESET}\n"
             f"FORMAT: dd-mm-yyyy\n"
             f"Not setting this flag uses the DEFAULT Date from the config",
        default=DATE_DEFAULT
    )

    parser.add_argument(
        "-due_date",
        type=str,
        help=f"{GREEN}Data until this Date will be used{RESET}\n"
             f"FORMAT: dd-mm-yyyy\n",
        default=DUE_DATE_DEFAULT
    )

    parser.add_argument(
        "-z", "--zone",
        type=int,
        help=f"{GREEN}Set the Zone to predict{RESET}\n"
             f"Either Zone 4 (default) or 8",
        choices=[4, 8],
        default=4
    )

    parser.add_argument("-m", "--mode",
                        type=str,
                        help=f"{GREEN}Set Mode For Predictions{RESET}\n"
                             "'SVR' - Support Vector Machines Classifier\n"
                             "'KNN' - K-Nearest Neighbors\n",
                        choices=["SVC", "KNN"],
                        default="KNN")

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.extract and (args.server == "both" or args.server == "live") and not args.player_list:
        logger.error("Set '-pl' or '--playerlist' Flag If Extracting Matches From Live Servers!")
        parser.exit()

    if args.predict and len(args.maps) != 1:
        logger.error("'-maps' Flag Issue: Specify Exactly One Map!")
        parser.exit()


    return args
# endregion
