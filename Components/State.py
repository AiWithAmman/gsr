import json
import os


class SettingsStore:
    def __init__(self, path):
        self.path= path
        self.data={}
        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded= json.load(f)
            if isinstance(loaded, dict):
                self.data= loaded
        except (OSError, ValueError):
            self.data={}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key]= value
        self.save()

    def save(self):
        try:
            tmp= self.path+".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, sort_keys=True)
            os.replace(tmp, self.path)
        except OSError:
            pass
