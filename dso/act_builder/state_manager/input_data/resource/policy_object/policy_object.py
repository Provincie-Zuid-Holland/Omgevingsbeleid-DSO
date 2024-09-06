import uuid
from datetime import datetime
from typing import Any


class PolicyObject:
    def __init__(self, data: dict):
        self.data: dict = data

    def get(self, key: str, default: Any = None):
        return self.data.get(key, default)

    def to_dict(self):
        serializable_dict = {}
        for key, value in self.data.items():
            if isinstance(value, uuid.UUID):
                serializable_dict[key] = str(value)
            elif isinstance(value, datetime):
                serializable_dict[key] = value.isoformat()
            else:
                serializable_dict[key] = value
        return serializable_dict
