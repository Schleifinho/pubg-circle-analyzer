import logging
import colorlog
from config.config import LOGGING_LEVEL

# Create a custom logger
logger = logging.getLogger("my_custom_logger")
logger.setLevel(LOGGING_LEVEL)

# Create a color formatter with custom formatting
formatter = colorlog.ColoredFormatter(
    (
        "%(log_color)s[%(asctime)s]%(reset)s "
        "%(log_color)s[%(levelname)-8s] "
        "%(message)s%(reset)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
