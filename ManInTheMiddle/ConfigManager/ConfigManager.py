import json
import os

class ConfigManaager():
    def __init__(self):
        self.setup()

    def setup(self):
        path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(path, "config.json")
        f = open(full_path)
        self.entries = json.load(f)