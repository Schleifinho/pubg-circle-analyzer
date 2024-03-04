# PUBG Circle Analyzer Tool

The PUBG Circle Analyzer Tool is a versatile command-line utility designed to help you analyze and visualize PUBG (PlayerUnknown's Battlegrounds) end-circle heatmaps, land ratios, and predict future zones. Whether you're a PUBG player looking to enhance your strategic planning or a tournament organizer seeking valuable insights, this tool provides the functionality you need.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Getting Started](#getting-started)
- [Options](#options)
- [Example Use Cases](#example-use-cases)
- [Adding Your PUBG API Code](#adding-your-pubg-api-code)
- [Database Configuration and Usage](#database-configuration-and-usage)
- [Customizing Configuration Settings](#customizing-configuration-settings)
- [License](#license)

## Features

- **Initialization:** Set up the necessary database and folders to store your PUBG circle data.
- **Tournament Data Retrieval:** Fetch tournament data, including player information and match results.
- **Circle Extraction:** Extract circle data from PUBG matches, for live or event server.
- **Heatmap Generation:** Create heatmaps to visualize circle-4 or end-circle data, showing where matches tend to conclude.
- **Circle Prediction:** Predict future circles starting from Zone 3, offering insights to enhance strategic decision-making.
- **Histogram Creation:** Generate histograms to analyze land ratios, aiding in understanding match dynamics.

## Usage

The tool offers several command-line options to perform various actions. Here are the primary usage options:

- Initialize the database and folders.
- Fetch tournament data.
- Extract circle data from matches (live or event server).
- Create heatmaps to visualize circle data.
- Generate histograms to visualize land ratios.
- Predict future circles.

Detailed usage instructions are available in the command-line help (use `main.py -h`).

## Getting Started

1. **Installation:** Clone this repository and ensure you have Python installed on your system.

2. **Setup:** Run `main.py -i` to initialize the database and folders.

3. **Data Retrieval:** Use `main.py -t` to fetch tournament data, or `main.py -e` to extract circle data from tournament or live matches. You can specify maps and other optional parameters.

4. **Visualization:** Create heatmaps with `main.py -c` and predict circles with `main.py -p`. Adjust prediction zones and modes as needed.

5. **Analysis:** Generate histograms with `main.py -hist` to analyze circle distribution.

6. **Player List:** To focus add matches from specific players, provide a list of player IDs with the `-pl` option.

## Options

- `-h, --help`: Display the help message.
- `-i, --init`: Initialize DB and Folders.
- `-t, --tournaments`: Fetch Tournaments.
- `-e, --extract`: Extract Circles (Optional Flag: '-maps').
- `-c, --heatmaps`: Create Heatmaps (Optional Flag: '-maps').
- `-p, --predict`: Predict Circles (Starting from Zone 3, predict Zone 4 or 8).
- `-hist, --histogram`: Create Histogram (Create Histogram for Zone 4 or 8).
- `-pl PLAYER_LIST [PLAYER_LIST ...]`: Specify a list of player IDs.
- `-z {4,8}, --zone {4,8}`: Set the Zone to predict (Either Zone 4 or 8).
- `-m {SVC,KNN}, --mode {SVC,KNN}`: Set Mode For Predictions ('SVC' - Support Vector Machines Classifier, 'KNN' - K-Nearest Neighbors).
- `-t_ids TOURNAMENT_IDS [TOURNAMENT_IDS ...]`: Manually add tournament IDs.
- `-t_type {tournament,scrim}`: Choose between tournament and scrim data.
- `-server {esport,live,both}`: Specify the data source server (esport, live, both).
- `-maps {vikendi,miramar,erangel,deston,taego} [{vikendi,miramar,erangel,deston,taego} ...]`: Choose specific PUBG maps.
- `-date DATE`: Set a custom start date for match analysis.
- `-t_ids TOURNAMENT_IDS [TOURNAMENT_IDS ...]`: Manually add tournament IDs.
- `-t_type {tournament,scrim}`: Choose between tournament and scrim data.
- `-server {esport,live,both}`: Specify the data source server (esport, live, both).
- `-maps {vikendi,miramar,erangel,deston,taego} [{vikendi,miramar,erangel,deston,taego} ...]`: Choose specific PUBG maps.

## Example Use Cases

1. **Fetching tournament Organizers:** To fetch all event tournaments and scrims that occurred since a specified date, use the `-t` option. This command will retrieve tournament data from the PUBG API based on your configured date. Please be aware that you can add tournament IDs manually using the `-t_ids` option, but the tool does not validate if they are valid tournament IDs.
Here's an example command:

    ```shell
    python3 ./main.py -t -date 01-01-2023
    python3 ./main.py -t -t_ids test-plh -t_type scrim

2. **Extracting circles:** To extract circles from live matches or tournament matches, use the `-e` option. This command allows you to gather circle data from either live matches or specific tournament matches.
Here are some examples:
    ```shell
   python3 ./main.py -e -server esport 
   python3 ./main.py -e -server esport -t_ids tournament_id1 tournament_id2 ...
   
   python3 ./main.py -e -server live -pl playername1 playername2 ... 
   
3. **Generate Heatmaps :** You can use the `-c` option to generate heatmaps that visualize the distribution of end-circle data. Heatmaps provide valuable insights into where matches tend to conclude on a specific PUBG map. Below are examples of generating heatmaps:
To generate heatmaps for a single PUBG map, specify the map using the `-maps` option. For example, if you want to create a heatmap for the "Erangel" map, use the following command:
   ```shell
   python3 ./main.py -c -server both -maps erangel
   
4. **Predict Circles :** Predicting Circles for a Specific Map. When predicting circles, you need to specify exactly one PUBG map for which you want to make predictions. You can choose to predict circles for Zone 4. Here's how to predict circles for a specific map:
Predicting Circles for Zone 4:
To predict circles starting from Zone 3 and progressing to Zone 4 (the default prediction) for a specific PUBG map, use the following command as an example:

    ```shell
    python3 ./main.py -p -maps erangel
   
5. **Generate Land Ratio Maps:** To generate land ratio maps for all available PUBG maps, you can use the following command as an example:
    ```shell
    python3 ./main.py -hist -server both
   
6. **Please note that many more options can be set to tailor the tool to your specific needs
To see better descriptions of available options and explore further customizations, you can use the -h command**

    ```shell
    python3 ./main.py -h
   
## Adding Your PUBG API Code

To use the PUBG Circle Analyzer Tool effectively, you need to add your PUBG API key to the `pubg_api_config.py` file. This API key is required for accessing PUBG match data and other game-related information. Follow these steps to set up your API key:

1. **Obtain a PUBG API Key:** If you don't already have a PUBG API key, you can obtain one by visiting the PUBG Developer Portal at [PUBG Developer Portal](https://developer.pubg.com/). Sign in or create an account, and then create a new API key.

2. **Access the `pubg_api_config.py` File:** Locate the `pubg_api_config.py` file within your PUBG Circle Analyzer Tool project directory.

3. **Edit the `pubg_api_config.py` File:** Open the `pubg_api_config.py` file in a text editor of your choice.

4. **Add Your API Key:** Inside the file, you'll see a variable named `API_KEY`. Set its value to your PUBG API key. It should look like this:

   ```python
   API_KEY = "your_api_key_here"

## Database Configuration and Usage

The PUBG Circle Analyzer Tool utilizes a MySQL database to store match data and other essential information. This chapter provides an overview of the database setup, including how to configure your MySQL database using `db_config.py`, and how the tool interacts with the database via the Peewee ORM.

### Setting Up the Database Configuration

The database configuration is managed through the `db_config.py` file located in the `config` folder. This file allows you to specify the connection details for your MySQL database, such as the host, username, password, and database name. Ensure that you have a MySQL server running and accessible before configuring this file.

## Customizing Configuration Settings

The PUBG Circle Analyzer Tool allows you to customize various configuration settings to tailor its behavior to your specific needs. You can adjust these settings in the `config.py` and `histogram.py` files (`config` folder). Here are the key configurations you can modify:

### `config.py`

- **`DATE_DEFAULT`:** This setting in the `config.py` file allows you to specify the start date for the matches you want to analyze. By default, it is set to a date value. Update it to the desired start date in the format "dd-mm-yy" This is useful for filtering matches within a specific time frame.

- **`NUM_OF_THREADS`:** The `NUM_OF_THREADS` setting controls the number of threads used for processing tasks. By default, it is set to a specific number. Adjust this value to control the level of multithreading in your analysis. Increasing the number of threads can speed up data processing, but it might require more system resources.

### `histogram_config.py`

- **`THRESHOLD_RANGE`:**  It controls the threshold for land ratio calculations. By default, it is set to `0.75`, meaning that a position was not in the next circle 3 out of 4 times.

### `db_config.py`

- **`DATABASE`:**   Specifies the name of the MySQL database.
- **`USER`:**  Specifies the username for the MySQL database.
- **`PASSWORD`:**   Specifies the password associated with the username. 
- **`HOST`:**   Specifies the host or the server where the MySQL database is running.

After making any changes to these configuration settings, make sure to save the files. Your customizations will take effect the next time you run the tool. These customizations give you the flexibility to adapt the tool to your specific analysis requirements and computing resources.

## License

This PUBG Circle Analyzer Tool is available under the **Creative Commons Attribution 4.0 International License**. This license requires that you provide proper attribution to the original author when you use, modify, or distribute this tool.

Please review the [LICENSE.md](LICENSE.md) file for the full text of the Creative Commons Attribution 4.0 International License and details on how to provide proper attribution.