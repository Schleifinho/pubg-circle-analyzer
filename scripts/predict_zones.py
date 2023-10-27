# region Imports
from datetime import datetime
import cv2
import numpy as np
import pandas as pd
from sklearn import svm
import matplotlib.pylab as plt

from config.config import DATE_FORMAT, ASSETS_FOLDER, WINDOW_SIZE, CIRCLE_3_SIZE, CIRCLE_4_SIZE, PUBG_MAP_SIZE
from db.fetching_db import fetch_live_server_telemetry_by_zones, \
    fetch_live_server_matches, fetch_event_server_matches, fetch_event_server_telemetry_by_zones, fetch_matches, \
    fetch_telemetry_data_poison_zone_per_phase
from helper.my_logger import logger
from helper.pubg_helper_functions import pubg_unit_to_pixel, pixel_to_pubg_unit

# endregion


# Initialize variables to store mouse coordinates
mouse_x, mouse_y = -1, -1
mouse_x_candidate, mouse_y_candidate = -1, -1


# Function to handle mouse events
def get_mouse_position(event, x, y, flags, param):
    global mouse_x, mouse_y
    global mouse_x_candidate, mouse_y_candidate
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y
    elif event == cv2.EVENT_LBUTTONDOWN:
        mouse_x_candidate, mouse_y_candidate = x, y




def train_svm(end_circles):
    logger.info(f"Training Model...")
    df = pd.DataFrame(columns=['x_before_zone', 'y_before_zone', 'x_predict_zone', 'y_predict_zone'], data=end_circles)

    train_data = df[['x_before_zone', 'y_before_zone']].values
    predict_x = df['x_predict_zone'].values
    predict_y = df['y_predict_zone'].values

    svc_x = svm.SVC(kernel="poly")
    svc_y = svm.SVC(kernel="poly")

    svc_x.fit(train_data, predict_x)
    svc_y.fit(train_data, predict_y)

    logger.info(f"Done")
    return svc_x, svc_y


def load_bg_image_and_resize(map_name):
    img_org = plt.imread(f"{ASSETS_FOLDER}/{map_name}.png")
    img_rgba = cv2.cvtColor(img_org, cv2.COLOR_BGRA2RGBA)
    img_resized = cv2.resize(img_rgba, (WINDOW_SIZE, WINDOW_SIZE))

    overlay = img_resized.copy()

    rows, cols = img_resized.shape[:2]
    cell_size = WINDOW_SIZE // 80  # Adjust the size of each cell

    color1 = (1, 1, 1)
    color2 = (.5, .5, .5)
    # Draw grid lines
    for i in range(0, rows, cell_size):
        if i % (cell_size * 10) == 0:
            cv2.line(overlay, (0, i), (cols, i), color1, 1)  # Draw white horizontal lines
        else:
            cv2.line(overlay, (0, i), (cols, i), color2, 1)  # Draw white horizontal lines

    for j in range(0, cols, cell_size):
        if j % (cell_size * 10) == 0:
            cv2.line(overlay, (j, 0), (j, rows), color1, 1)  # Draw white vertical lines
        else:
            cv2.line(overlay, (j, 0), (j, rows), color2, 1)  # Draw white vertical lines

    result = cv2.addWeighted(overlay, 0.33, img_resized, 1, 0)

    return result


def draw_circle_at(img, x, y, radius, color):
    cv2.circle(img, (x, y), radius, color, -1)


def start_predict_loop(background_image, svc_x, svc_y, window_name):
    global mouse_x_candidate
    global mouse_y_candidate
    circle_predict_image = get_circle_overlay_image(background_image)

    circle_predict_color = (0.0, 0.0, 1.0)
    circle_live_color = (1.0, 0.0, 0.0)

    pixel_radius_circle_3 = pubg_unit_to_pixel(CIRCLE_3_SIZE)
    pixel_radius_circle_4 = pubg_unit_to_pixel(CIRCLE_4_SIZE)

    while True:
        # Copy the original image to avoid overwriting the drawn circle
        img = background_image.copy()

        circle_at_mouse_image = np.zeros(img.shape, dtype=np.float32)
        circle_at_mouse_image[:, :, 3] = 0.5

        # Draw a circle at the mouse position
        if mouse_x != -1 and mouse_y != -1:
            draw_circle_at(circle_at_mouse_image, mouse_x, mouse_y, pixel_radius_circle_3, circle_live_color)

        # Draw a circle at the mouse position
        if mouse_x_candidate != -1 and mouse_x_candidate != -1:
            circle_predict_image = get_circle_overlay_image(background_image)
            x_pubg = pixel_to_pubg_unit(mouse_x_candidate)
            y_pubg = pixel_to_pubg_unit(mouse_y_candidate)

            middle_x = pubg_unit_to_pixel(svc_x.predict([(x_pubg, y_pubg)]))
            middle_y = pubg_unit_to_pixel(svc_y.predict([(x_pubg, y_pubg)]))

            draw_circle_at(circle_predict_image, mouse_x_candidate, mouse_y_candidate, pixel_radius_circle_3,
                           circle_live_color)
            draw_circle_at(circle_predict_image, middle_x, middle_y, pixel_radius_circle_4, circle_predict_color)
            mouse_x_candidate = mouse_y_candidate = -1

        circle_image = cv2.addWeighted(circle_at_mouse_image, 1, circle_predict_image, 1, 0)
        # Display the image

        result = cv2.addWeighted(background_image, 1, circle_image, 1, 0)
        cv2.imshow(window_name, result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # Press 'q' to quit
            break
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    cv2.destroyAllWindows()


def get_circle_overlay_image(background_image):
    img = np.zeros(background_image.shape, dtype=np.float32)
    img[:, :, 3] = 0.5
    return img


def open_predict_window(map_name, svc_x, svc_y):
    background_image = load_bg_image_and_resize(map_name)

    window_name = f"Predict: {map_name.upper()}"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, get_mouse_position)

    if background_image is None:
        logger.error(f"{ASSETS_FOLDER}/{map_name}.png does not exist!")
    else:
        start_predict_loop(background_image, svc_x, svc_y, window_name)


def start_predicting_circles(server, use_map, zone, date_string):
    date = datetime.strptime(date_string, DATE_FORMAT)
    matches_esport_live = fetch_matches(server, use_map[0], date)
    map_pretty = use_map[0].lower()

    zones = [zone - 1, zone]
    zone_start_and_predict = fetch_telemetry_data_poison_zone_per_phase(server, matches_esport_live, zones)

    zone_start_and_predict_filtered = []
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
            x_before_zone, x_predict_zone = poison_gas_x_group_string.split(",")
            y_before_zone, y_predict_zone = poison_gas_y_group_string.split(",")
            zone_start_and_predict_filtered.append(
                {"x_before_zone": int(float(x_before_zone)), "y_before_zone": int(float(y_before_zone)),
                 "x_predict_zone": int(float(x_predict_zone)), "y_predict_zone": int(float(y_predict_zone))})
        except Exception as e:
            print(e)

    logger.info(F"# Matches: {len(zone_start_and_predict_filtered)}")
    svc_x, svc_y = train_svm(zone_start_and_predict_filtered)
    open_predict_window(map_pretty, svc_x, svc_y)
