"""
Memory Manager: Handles long-term and short-term memory, event logs, and context.
"""
import json
import os

class MemoryManager:
    def __init__(self, ltm_path='ltm.json', stm_path='stm.json'):
        self.ltm_path = ltm_path
        self.stm_path = stm_path
        self.ltm = self._load(self.ltm_path)
        self.stm = self._load(self.stm_path)

    def _load(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def save(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def write_ltm(self, key, value):
        self.ltm[key] = value
        self.save(self.ltm_path, self.ltm)

    def get_ltm(self):
        return self.ltm

    def write_stm(self, key, value):
        self.stm[key] = value
        self.save(self.stm_path, self.stm)

    def get_stm(self):
        return self.stm
