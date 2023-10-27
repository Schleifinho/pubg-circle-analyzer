from config.config import WINDOW_SIZE, PUBG_MAP_SIZE


def pixel_to_pubg_unit(pixel):
    return pixel / WINDOW_SIZE * PUBG_MAP_SIZE


def pubg_unit_to_pixel(pubg_unit):
    return int(pubg_unit / PUBG_MAP_SIZE * WINDOW_SIZE)
