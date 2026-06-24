from pathlib import Path
import os
import json

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

def move_file():
    ...
if __name__ == "__main__":
    # config = load_config()
    # rules = config["rules"]
    # unknown = config["unknown_folder"]
    # print(get_destination("resume.pdf", rules, unknown))
    # print(get_destination("photo.JPG", rules, unknown))
    # print(get_destination("something.xyz", rules, unknown))
    # print(get_destination("movie.mp4", rules, unknown))

    test_path = Path('test-resume.pdf')
    test_path.touch()   # it creates an empty file with that name
    result = handle_duplicate(test_path)
    print(result)

    test_path.unlink()