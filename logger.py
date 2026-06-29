import logging
from pathlib import Path
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

def setup_logger():
    logs_dir = get_base_path() / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "activity.log"

    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.DEBUG)

    # format for the log files
    formatter = logging.Formatter(
        fmt = "%(asctime)s - %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    # wrinting to the log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # writing to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger