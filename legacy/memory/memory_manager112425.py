import json
import os

MEMORY_DIR = "nyra_memory"
STM_PATH = os.path.join(MEMORY_DIR, "stm.json")
WM_PATH  = os.path.join(MEMORY_DIR, "wm.json")
LTM_PATH = os.path.join(MEMORY_DIR, "ltm.json")


class MemoryManager:
    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self._init_file(STM_PATH)
        self._init_file(WM_PATH)
        self._init_file(LTM_PATH)

    def _init_file(self, path):
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({}, f)

    def load(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def save(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    # PUBLIC GETTERS
    def get_stm(self):
        return self.load(STM_PATH)

    def get_wm(self):
        return self.load(WM_PATH)

    def get_ltm(self):
        return self.load(LTM_PATH)

    # PUBLIC WRITERS
    def write_stm(self, key, value):
        data = self.get_stm()
        data[key] = value
        self.save(STM_PATH, data)

    def write_wm(self, key, value):
        data = self.get_wm()
        data[key] = value
        self.save(WM_PATH, data)

    def write_ltm(self, key, value):
        data = self.get_ltm()
        data[key] = value
        self.save(LTM_PATH, data)
