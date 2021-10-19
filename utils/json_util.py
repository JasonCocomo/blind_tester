import json


def load_json(config_path: str):
    with open(config_path, 'r') as config_file:
        config_dict = json.load(config_file)
    return config_dict
