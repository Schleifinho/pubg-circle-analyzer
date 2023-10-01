# region Imports
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
from tqdm import tqdm

from config.config import RESULTS_FOLDER, DATE_FORMAT
from db.fetching_db import fetch_matches, fetch_telemetry_data
from helper.my_logger import logger
plt.style.use("seaborn")
# endregion

# region Create Heatmaps
def create_heat_maps(server, maps, date_string):
    date = datetime.strptime(date_string, DATE_FORMAT)

    for map_i in tqdm(maps, desc="Generating for Map...", colour="green"):
        logger.debug(f"\nGenerating {map_i[1]}")
        matches_esport_live = fetch_matches(server, map_i[0], date)
        selection = fetch_telemetry_data(server, matches_esport_live)

        if len(selection) == 0:
            logger.info(f"No telemetry data for {map_i[1]} [{server}]!")
            continue

        circles = [{"x": match.poisonGasWarningPositionX, "y": match.poisonGasWarningPositionY} for match in selection]


        server_name = "E-SPORT" if server == "esport" else "LIVE" if server == "live" else "E-SPORT/LIVE"
        title = f"2023 {server_name} " + map_i[1] + " (# maps: " + str(len(circles)) + ")"
        create_heat_map_for_end_circles(circles, map_i, server, title, bw_adjust=0.5)
        create_heat_map_for_end_circles(circles, map_i, server, title, bw_adjust=0.33)


def create_heat_map_for_end_circles(circles, map_tuple, server, title, bw_adjust=1.0):
    df = pd.DataFrame(columns=['x', 'y'], data=circles)

    df['x'] = df['x'] * 0.00001
    df['y'] = df['y'] * 0.00001

    map_name = map_tuple[0].lower()
    map_name_pretty = map_tuple[1].lower()

    img = plt.imread(f"assets/{map_name}.png")
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

    sns.kdeplot(data=df, x='x', y='y', fill=True, alpha=0.5, legend=True, levels=50, gridsize=400, ax=ax,
                bw_adjust=bw_adjust, cmap='Spectral_r', cbar=True, warn_singular=False)  # turbo

    folder = f"{RESULTS_FOLDER}/{server}/{map_name_pretty}/"
    plt.savefig(folder + map_name_pretty + '_heatmap_' + str(bw_adjust).replace(".", "_") + '.png')

    sns.scatterplot(data=df, x='x', y='y', s=75, label="End Circles", marker='o', edgecolor="white")

    lgnd = ax.legend(bbox_to_anchor=(1.35, 1))
    lgnd.legendHandles[0].set_sizes([100])
    plt.savefig(folder + map_name_pretty + '_heatmap_' + str(bw_adjust).replace(".", "_") + '_points.png')
# endregion
