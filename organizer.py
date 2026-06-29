from pathlib import Path
import json
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from logger import setup_logger
from notifier import send_notification
from utils import format_file_size
import threading

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

logger = setup_logger()

def load_config():
    config_path = get_base_path() / "config.json"
    with open(config_path, 'r') as f:
        config = json.load(f)

    if not config["watch_folder"]:
        config["watch_folder"] = str(Path.home() / "Downloads")
    
    if "first_run" not in config:
        config["first_run"] = True

    return config

def get_destination(filename, rules, unknown_folder):
    extension = Path(filename).suffix.lower()
    if extension in rules:
        return rules[extension]
    else:
        return unknown_folder
    
def handle_duplicate(destination_path):
    if not destination_path.exists():
        return destination_path
    
    stem = destination_path.stem
    suffix = destination_path.suffix
    parent = destination_path.parent
    counter = 1
    
    while True:
        new_name = f'{stem}_{counter}{suffix}'
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def move_file(source_path, watch_folder, rules, unknown_folder, dry_run=False, logger=None):
    destination_folder = get_destination(source_path.name, rules, unknown_folder)   # gets the destination folder name for this file
    destination_dir = Path(watch_folder) / destination_folder   # build the full destination directory path
    destination_path = destination_dir / source_path.name   # build full destination file path
    destination_path = handle_duplicate(destination_path)   # handling duplication

    if dry_run:
        # file_size = format_file_size(destination_path.stat().st_size())
        # logger.info(f"Moved {source_path} to {destination_path} ({file_size})")
        # send_notification(source_path.name, str(destination_path.parent))
        logger.info(f"[DRY RUN] Would move: {source_path.name}  to  {destination_path}")
        return
    
    # this creates the destination folder if doesnt exist
    destination_dir.mkdir(parents = True, exist_ok = True)

    shutil.move(str(source_path), str(destination_path))
    # print(f"Moved {source_path.name} to {destination_path}")
    file_size = format_file_size(destination_path.stat().st_size)
    logger.info(f"Moved: {source_path.name}  to  {destination_path}  ({file_size})")
    send_notification(source_path.name, str(destination_path.parent))


class FileHandler(FileSystemEventHandler):
    def __init__(self, watch_folder, rules, unknown_folder, dry_run=False, logger=None):
        self.watch_folder = watch_folder
        self.rules = rules
        self.unknown_folder = unknown_folder
        self.dry_run = dry_run
        self.logger = logger
    
    def on_created(self, event):
        if event.is_directory:
            return
        source_path = Path(event.src_path)

        ignored_extensions = {".tmp", ".crdownload", ".part", ".download"}
        ignored_prefixes = ("~", ".")

        if source_path.suffix.lower() in ignored_extensions:
            return
        if source_path.name.startswith(ignored_prefixes):
            return
        
        self._wait_for_file(source_path)

        if not source_path.exists():
            return

        move_file(
            source_path,
            self.watch_folder,
            self.rules,
            self.unknown_folder,
            self.dry_run,
            self.logger
        )
    
    def on_moved(self, event):
        if event.is_directory:
            return
        
        source_path = Path(event.dest_path)

        ignored_extensions = {".tmp", ".crdownload", ".part", ".download"}
        ignored_prefixes = ("~", ".")

        # checks
        if source_path.suffix.lower() in ignored_extensions:
            return
        if source_path.name.startswith(ignored_prefixes):
            return
        if not source_path.exists():
            return
        
        move_file(
            source_path,
            self.watch_folder,
            self.rules,
            self.unknown_folder,
            self.dry_run,
            self.logger
        )

    def _wait_for_file(self, path):
        previous_size = -1
        while True:
            try:
                current_size = path.stat().st_size
                if current_size == previous_size:
                    break
                previous_size = current_size
                time.sleep(1)
            except FileNotFoundError:
                break

def start_watching(dry_run=False):
    config = load_config()
    watch_folder = config["watch_folder"]
    rules = config["rules"]
    unknown_folder = config["unknown_folder"]

    if config.get("first_run", True):
        try:
            from autostart import enable_autostart
            enable_autostart()
            logger.info("First Launch - Autostart Enabled")
        except Exception as e:
            logger.warning(f"Could not enable autostart: {e}")
        finally:
            config["first_run"] = False
            config_path = get_base_path() / "config.json"
            with open (config_path, "w") as f:
                json.dump(config, f, indent=2)

    stop_event = threading.Event()

    handler = FileHandler(watch_folder, rules, unknown_folder, dry_run, logger)
    observer = Observer()
    observer.schedule(handler, watch_folder, recursive=False)

    logger.info(f"Watching the folder {watch_folder}")
    logger.info("Press Ctrl + c to stop\n")

    observer.start()

    from tray import run_tray
    tray_thread = threading.Thread(
        target=run_tray,
        args=(stop_event, watch_folder),
        daemon=True
    )
    tray_thread.start()

    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
        logger.info("File Organizer Stopped")

if __name__ == "__main__":
    import sys
    # dry_run = "--dry-run" in sys.argv
    # start_watching(dry_run=dry_run)
    if "--update" in sys.argv:
        from autostart import enable_autostart
        enable_autostart()
        print("Autostart path updated.")
    else:
        dry_run = "--dry-run" in sys.argv
        start_watching(dry_run=dry_run)