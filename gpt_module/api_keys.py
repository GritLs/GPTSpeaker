import os
import json

class ApiKeys:
    def __init__(self, file_path='./keys.json'):
        self.file_path = file_path
        self.keys = self.load_keys()

    def load_keys(self):
        with open(self.file_path, 'r') as f:
            keys = json.load(f)
        return keys

    def set_key_as_env_var(self, key):
        if key in self.keys:
            os.environ[key] = self.keys[key]
        else:
            raise KeyError(f"Key '{key}' not found in {self.file_path}")

    def get_key(self, key):
        if key in self.keys:
            return self.keys[key]
        else:
            raise KeyError(f"Key '{key}' not found in {self.file_path}")

    def set_all_keys_as_env_vars(self):
        for key in self.keys:
            os.environ[key] = self.keys[key]

