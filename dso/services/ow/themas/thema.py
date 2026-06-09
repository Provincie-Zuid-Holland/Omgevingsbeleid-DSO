from typing import List

from dso.services.ow.themas.gen import themas
from dso.services.ow.themas.types import Thema


class ThemaFactory:
    def __init__(self):
        self._data = themas

    def get_keys(self) -> List[str]:
        return list(self._data.keys())

    def get_thema_by_key(self, key: str) -> Thema:
        return self._data[key]
