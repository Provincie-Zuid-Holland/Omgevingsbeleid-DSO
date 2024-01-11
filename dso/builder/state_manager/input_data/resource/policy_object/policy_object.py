from typing import Any


class PolicyObject:
    def __init__(self, data: dict):
        self.data: dict = data

    def get(self, key: str, default: Any = None):
        return self.data.get(key, default)
