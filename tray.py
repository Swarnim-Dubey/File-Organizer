import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import os
from pathlib import Path
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

def create_icon_image():
    image = Image.new("RGB", (64, 64), color=(37, 99, 235))
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    return image

def open_log_file():
    log_path = get_base_path() / "logs" / "activity.log"
    if log_path.exists():
        os.startfile(str(log_path))

def build_tray(stop_event, watch_folder):
    icon_image = create_icon_image()
    menu = pystray.Menu(
        item(f"Watching : {Path(watch_folder).name}", None, enabled=False),
        pystray.Menu.SEPARATOR,
        item("Open Log File", lambda: open_log_file()),
        item("Exit", lambda: stop_event.set())
    )

    icon = pystray.Icon(
        name="File Organizer",
        icon=icon_image,
        title="File Organizer",
        menu=menu
    )

    return icon

def run_tray(stop_event, watch_folder):
    icon = build_tray(stop_event, watch_folder)
    icon.run_detached()

    stop_event.wait()
    icon.stop()
