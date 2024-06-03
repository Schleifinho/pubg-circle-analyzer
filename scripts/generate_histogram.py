from datetime import datetime
import cv2
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
from config.config import DATE_FORMAT, CIRCLE_4_SIZE, ASSETS_FOLDER, CIRCLE_3_SIZE, HISTOGRAMS_FOLDER, WINDOW_SIZE
from config.histogram_config import THRESHOLD_RANGE, COLOR_WHITE, COLOR_BLACK
from db.fetching_db import fetch_matches, fetch_telemetry_data_poison_zone_per_phase
from helper.legend_line import LegendLine
from helper.my_logger import logger
from helper.pubg_helper_functions import pubg_unit_to_pixel


def load_bg_image_and_resize(map_name):
    img_org = plt.imread(f"{ASSETS_FOLDER}/{map_name}.png")
    img_rgba = cv2.cvtColor(img_org, cv2.COLOR_BGRA2RGBA)
    img_resized = cv2.resize(img_rgba, (WINDOW_SIZE, WINDOW_SIZE))
    return img_resized


def add_credits_to_legend(res, width, height):
    line = (width - 90, height - 10)
    font_color = (0.25, 0.25, 0.25)
    font_scale = 0.5
    font_thickness = 1
    font_line_type = cv2.FONT_ITALIC

    cv2.putText(res, "@Schleifinho", line, cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, font_color, font_thickness,
                font_line_type)

    return res


def prepare_legend_background(res_shape, width, height):
    background = np.zeros(res_shape, dtype=np.float32)
    background[0: height, 0: width] = 1
    return background


def add_color_map_to_bg(res, width, line_num, line_width_padding, line_height_padding):
    colormap_jet = cv2.imread(f"{ASSETS_FOLDER}/colorscale_jet.jpg")
    colormap_jet = cv2.resize(colormap_jet, (width - 2 * line_width_padding, line_height_padding))
    h, w, _ = colormap_jet.shape
    jet_height = int(line_num * line_height_padding)
    jet_width = line_width_padding
    res[jet_height:jet_height + h, jet_width:jet_width + w] = colormap_jet / 255
    return res


def add_legend_to_image(res, circles_len, date, due_date, match_type):
    lines = [LegendLine(f"Number Of Maps: {circles_len} ({match_type})", scale=.9),
             LegendLine(f"From: {date}"),
             LegendLine(f"To: {due_date}"),
             LegendLine("Not In Zone 4 Percentage"),
             LegendLine(f"{int(THRESHOLD_RANGE * 100)}%                   100%", color=COLOR_WHITE)]
    width = 375
    height = 180
    line_height_padding = 30
    line_width_padding = 25

    background = prepare_legend_background(res.shape, width, height)
    res = cv2.addWeighted(background, .67, res, 1, 0)
    res = add_color_map_to_bg(res, width, 4.4, line_width_padding, line_height_padding)

    for index, legend_line in enumerate(lines):
        line = (line_width_padding, (index + 1) * line_height_padding)
        cv2.putText(res, legend_line.text, line, legend_line.font, legend_line.scale, legend_line.color,
                    legend_line.font_thickness, legend_line.font_line_type)

    res = add_credits_to_legend(res, width, height)
    return res


def create_histogram(circles, map_name_tuple, server, date, due_date, match_type):
    map_name = map_name_tuple[0].lower()
    map_name_pretty = map_name_tuple[1].lower()
    histogram_zone_3 = np.zeros((WINDOW_SIZE, WINDOW_SIZE), dtype=np.uint32)
    histogram_shifts = np.zeros((WINDOW_SIZE, WINDOW_SIZE), dtype=np.uint32)
    radius_z4 = pubg_unit_to_pixel(CIRCLE_4_SIZE)
    radius_z3 = pubg_unit_to_pixel(CIRCLE_3_SIZE)

    # Create a blank image
    for circle in circles:
        circle_zone_3 = np.zeros((WINDOW_SIZE, WINDOW_SIZE), dtype=np.uint8)
        circle_shift = np.zeros((WINDOW_SIZE, WINDOW_SIZE), dtype=np.uint8)
        x_pos_z3 = pubg_unit_to_pixel(circle['x_zone_3'])
        y_pos_z3 = pubg_unit_to_pixel(circle['y_zone_3'])
        x_pos_z4 = pubg_unit_to_pixel(circle['x_zone_4'])
        y_pos_z4 = pubg_unit_to_pixel(circle['y_zone_4'])

        cv2.circle(circle_zone_3, (x_pos_z3, y_pos_z3), radius_z3, COLOR_WHITE, -1)
        cv2.circle(circle_shift, (x_pos_z3, y_pos_z3), radius_z3, COLOR_WHITE, -1)
        cv2.circle(circle_shift, (x_pos_z4, y_pos_z4), radius_z4, COLOR_BLACK, -1)

        histogram_zone_3 += circle_zone_3
        histogram_shifts += circle_shift

    histogram_zone_3[histogram_zone_3 == 0] = 1
    histogram_shifts[histogram_shifts == 0] = 0

    histogram = (histogram_shifts / histogram_zone_3)
    histogram[histogram < THRESHOLD_RANGE] = 0

    kernel_size = 5  # Adjust this as needed
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    histogram = cv2.morphologyEx(histogram, cv2.MORPH_CLOSE, kernel)

    # Get the minimum value greater than 0
    mask = histogram > 0
    min_val = histogram[mask].min()
    max_val = np.max(histogram)
    normalized_histogram = ((histogram - min_val) / (max_val - min_val))
    normalized_histogram = np.clip(normalized_histogram, 0, 1)

    normalized_array = cv2.normalize(normalized_histogram, None, 0, 255, cv2.NORM_MINMAX)
    image_array = normalized_array.astype(np.uint8)

    # Create an empty output image
    colormap = cv2.applyColorMap(image_array, cv2.COLORMAP_JET)
    bg = load_bg_image_and_resize(map_name)
    mask = (mask > 0).astype(np.uint8) * 255
    colormap = cv2.bitwise_and(colormap, colormap, mask=mask)
    colormap = colormap.astype(np.float32) / 255
    bg = cv2.cvtColor(bg, cv2.COLOR_RGBA2RGB)

    res = cv2.addWeighted(colormap, 0.5, bg, 1, 0)
    res = add_legend_to_image(res, len(circles), date, due_date, match_type)

    percentage = str(THRESHOLD_RANGE).replace(".", "_")
    date_pretty = str(date).replace("-", "_")
    due_date_pretty = str(due_date).replace("-", "_")
    folder_and_name = f"{HISTOGRAMS_FOLDER}/{server}/{map_name_pretty}/{map_name}_{percentage}_{date_pretty}_{due_date_pretty}_{match_type}.jpg"
    cv2.imwrite(f"{folder_and_name}", res * 255)


def start_generating_histogram(server, maps, date_string, due_date_string, zone, match_type):
    date = datetime.strptime(date_string, DATE_FORMAT)
    due_date = datetime.strptime(due_date_string, DATE_FORMAT)

    for map_i in tqdm(maps, desc="Generating Histogram for Map...", colour="green"):
        logger.debug(f"\nGenerating {map_i[1]}")
        matches_esport_live = fetch_matches(server, map_i[0], date, due_date, match_type)

        phases = [zone - 1, zone]
        zone_start_and_predict = fetch_telemetry_data_poison_zone_per_phase(server, matches_esport_live, phases)
        zone_3_and_4 = []
        for z in zone_start_and_predict:
            poison_gas_x_group_string = z.poisonGasXGroup
            poison_gas_y_group_string = z.poisonGasYGroup

            if type(poison_gas_y_group_string) is not str or type(poison_gas_y_group_string) is not str:
                logger.debug("Corrupt Match! Like the match ended to early!")
                continue

            if poison_gas_x_group_string is None or poison_gas_y_group_string is None:
                logger.debug("Corrupt Match! Like the match ended to early!")
                continue
            if poison_gas_x_group_string.count(",") != 1 or poison_gas_y_group_string.count(",") != 1:
                logger.debug("Corrupt Match! Like the match ended to early!")
                continue

                # Data could be corrupted!
            try:
                x_before_zone, x_after_zone = poison_gas_x_group_string.split(",")
                y_before_zone, y_after_zone = poison_gas_y_group_string.split(",")
                zone_3_and_4.append(
                    {"x_zone_3": int(float(x_before_zone)), "y_zone_3": int(float(y_before_zone)),
                     "x_zone_4": int(float(x_after_zone)), "y_zone_4": int(float(y_after_zone))})
            except Exception as e:
                logger.debug(e)
        # Don't create hist if less than 5 circles        
        if len(zone_3_and_4) > 5:
            create_histogram(zone_3_and_4, map_i, server, date_string, due_date_string, match_type)
