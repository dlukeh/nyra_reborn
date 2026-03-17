
"""
Nyra Persistent Memory System
Saves conversation history and user preferences between sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path

MEMORY_DIR = "nyra_memory"
STM_PATH = os.path.join(MEMORY_DIR, "stm.json")
WM_PATH  = os.path.join(MEMORY_DIR, "wm.json")
LTM_PATH = os.path.join(MEMORY_DIR, "ltm.json")

class MemoryManager:
    def __init__(self):
        # expose paths as instance attributes
        self.STM_PATH = STM_PATH
        self.WM_PATH  = WM_PATH
        self.LTM_PATH = LTM_PATH

        os.makedirs(MEMORY_DIR, exist_ok=True)
        self._init_file(self.STM_PATH)
        self._init_file(self.WM_PATH)
        self._init_file(self.LTM_PATH)

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
        return self.load(self.STM_PATH)

    def get_wm(self):
        return self.load(self.WM_PATH)

    def get_ltm(self):
        return self.load(self.LTM_PATH)

    # PUBLIC WRITERS
    def write_stm(self, key, value):
        data = self.get_stm()
        data[key] = value
        self.save(self.STM_PATH, data)

    def write_wm(self, key, value):
        data = self.get_wm()
        data[key] = value
        self.save(self.WM_PATH, data)

    def write_ltm(self, key, value):
        data = self.get_ltm()
        data[key] = value
        self.save(self.LTM_PATH, data)
