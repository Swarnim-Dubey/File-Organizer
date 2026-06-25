from pathlib import Path
import os
import json
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

def load_config():
    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)
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

def move_file(source_path, watch_folder, rules, unknown_folder, dry_run=False):
    destination_folder = get_destination(source_path.name, rules, unknown_folder)   # gets the destination folder name for this file
    destination_dir = Path(watch_folder) / destination_folder   # build the full destination directory path
    destination_path = destination_dir / source_path.name   # build full destination file path
    destination_path = handle_duplicate(destination_path)   # handling duplication

    if dry_run:
        print(f"Dry run will move: {source_path} to {destination_path}")
        return
    
    # this creates the destination folder if doesnt exist
    destination_dir.mkdir(parents = True, exist_ok = True)

    shutil.move(str(source_path), str(destination_path))
    print(f"Moved {source_path.name} to {destination_path}")


class FileHandler(FileSystemEventHandler):
    def __init__(self, watch_folder, rules, unknown_folder, dry_run=False):
        self.watch_folder = watch_folder
        self.rules = rules
        self.unknown_folder = unknown_folder
        self.dry_run = dry_run
    
    def on_created(self, event):
        if event.is_directory:
            return
        source_path = Path(event.src_path)
        self._wait_for_file(source_path)

        move_file(source_path, self.watch_folder, self.rules, self.unknown_folder, self.dry_run)
    
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

    handler = FileHandler(watch_folder, rules, unknown_folder, dry_run)
    observer = Observer()
    observer.schedule(handler, watch_folder, recursive=False)

    print(f"Watching the folder {watch_folder}")
    print("Press Ctrl + c to stop\n")

    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped Watching !!")

    observer.join()

if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    start_watching(dry_run=dry_run)