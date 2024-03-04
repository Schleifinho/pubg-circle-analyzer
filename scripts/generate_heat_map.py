# region Imports
from datetime import datetime

import cv2
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
from tqdm import tqdm

from config.config import DATE_FORMAT, ASSETS_FOLDER, HEATMAPS_FOLDER
from db.fetching_db import fetch_telemetry_data, fetch_matches
from helper.legend_line import LegendLine
from helper.my_logger import logger
from scripts.generate_histogram import prepare_legend_background, add_credits_to_legend

# python3.7 (or lower?)
# plt.style.use("seaborn")
sns.set_style("whitegrid")


# endregion

# region Create Heatmaps
def create_heat_maps(server, maps, date_string, due_date_string, zone):
    date = datetime.strptime(date_string, DATE_FORMAT)
    due_date = datetime.strptime(due_date_string, DATE_FORMAT)

    for map_i in tqdm(maps, desc="Generating for Map...", colour="green"):
        logger.debug(f"\n{map_i[1]}")
        matches_esport_live = fetch_matches(server, map_i[0], date, due_date)
        selection = fetch_telemetry_data(server, matches_esport_live, zone, or_greater=False)

        if len(selection) == 0:
            logger.info(f"No telemetry data for {map_i[1]} [{server}]!")
            continue

        circles = [{"x": match.poisonGasWarningPositionX, "y": match.poisonGasWarningPositionY} for match in selection]

        logger.debug(f"Matches found: {len(circles)}")

        server_name = "E-SPORT" if server == "esport" else "LIVE" if server == "live" else "E-SPORT/LIVE"
        title = f"2023 {server_name} " + map_i[1] + " (# maps: " + str(len(circles)) + ")"
        create_heat_map_for_end_circles(circles, map_i, server, title, date_string, due_date_string, zone, bw_adjust=0.5)
        create_heat_map_for_end_circles(circles, map_i, server, title, date_string, due_date_string, zone, bw_adjust=0.33)


def create_heat_map_for_end_circles(circles, map_tuple, server, title, date, due_date, zone, bw_adjust=1.0):
    df = pd.DataFrame(columns=['x', 'y'], data=circles)

    df['x'] = df['x'] * 0.00001
    df['y'] = df['y'] * 0.00001

    map_name = map_tuple[0].lower()
    map_name_pretty = map_tuple[1].lower()

    img = plt.imread(f"{ASSETS_FOLDER}/{map_name}.png")
    fig, ax = plt.subplots(figsize=(16, 16))

    ticks = np.arange(0.0, 9, 1.02)

    ax.yaxis.set_ticks(ticks)
    ax.xaxis.set_ticks(ticks)
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0.5)
    ax.xaxis.tick_top()
    ax.set(ylim=(8.16, 0))
    ax.set(xlim=(0, 8.16))
    ax.imshow(img, extent=[0, 8.16, 8.16, 0])
    ax.text(0.5, 0.95, title, transform=ax.transAxes,
            fontsize=26, color='white', alpha=.75,
            ha='center', va='top')
    ax.text(0.125, 0.16, '@Schleifinho', transform=ax.transAxes,
            fontsize=26, color='white', alpha=0.25,
            ha='left', va='top')

    sns.kdeplot(data=df, x='x', y='y', fill=True, alpha=0.4, legend=True, levels=50, gridsize=400, ax=ax,
                bw_adjust=bw_adjust, cmap='Spectral_r', cbar=True, warn_singular=False)  # turbo

    date_pretty = str(date).replace("-", "_")
    due_date_pretty = str(due_date).replace("-", "_")
    bw_string = str(bw_adjust).replace(".", "")
    folder_and_name = f"{HEATMAPS_FOLDER}/{server}/{map_name_pretty}/{map_name_pretty}"\
                      f"_zone-{zone}_{bw_string}_from-{date_pretty}_to-{due_date_pretty}.jpg"

    plt.savefig(folder_and_name)

    sns.scatterplot(data=df, x='x', y='y', s=75, label="Zone Center", marker='o', edgecolor="white")

    lgnd = ax.legend(bbox_to_anchor=(1.35, 1))
    lgnd.legendHandles[0].set_sizes([100])

    folder_and_name = f"{HEATMAPS_FOLDER}/{server}/{map_name_pretty}/{map_name_pretty}" \
                      f"_zone-{zone}_bw-{bw_string}_from-{date_pretty}_to-{due_date_pretty}_points.jpg"
    plt.savefig(folder_and_name)


# endregion
