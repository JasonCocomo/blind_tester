
from utils.json_util import load_json


class ConfigWrapper:

    def __init__(self, config_path):
        self.config = load_json(config_path)

    def get(self, key, soft=False):
        if soft:
            return self.config.get(key)
        return self.config[key]
