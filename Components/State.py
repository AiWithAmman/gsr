import json
import datetime



class SettingsStore:
    def __init__(self, path):
        self.path= path
        self.data={}
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.data= json.load(f)
        except (OSError, ValueError):
            self.data={}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        old_value = self.data.get(key)

        if old_value == value:
            return
        
        self.data[key]= value
        
        if key.startswith(("diag.", "perm.", "security.", "general.", "speech.", "inking.", "activity.")):
            self.record_change(key, old_value, value)
        else:
            self.save()

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except OSError:
            pass

    def get_history(self):
        return self.data.get("_privacy_history",[])

    def add_listener(self, callback):
        if not hasattr(self, "listeners"):
            self.listeners = []
        self.listeners.append(callback)

    def record_change(self, key, old_value, new_value):

        history = self.data.setdefault("_privacy_history",[])

        event = { "key": key, "old_value": old_value, "new_value": new_value, 
            "timestamp": datetime.datetime.now().astimezone().isoformat(timespec = "seconds")}

        history.append(event)
        
        self.save()

        for callback in getattr(self, "listeners", []):
            callback(event)