import cv2

from config.histogram_config import COLOR_BLACK


class LegendLine:
    def __init__(self, text, color=COLOR_BLACK, scale=1, font=cv2.FONT_HERSHEY_COMPLEX_SMALL, font_thickness=1,
                 font_line_type=cv2.LINE_AA):
        self.text = text
        self.color = color
        self.scale = scale
        self.font = font
        self.font_thickness = font_thickness
        self.font_line_type = font_line_type
