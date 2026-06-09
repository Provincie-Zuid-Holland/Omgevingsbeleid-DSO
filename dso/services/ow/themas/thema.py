from typing import Dict

from dso.services.ow.themas.gen import themas
from dso.services.ow.themas.types import Thema


class ThemaFactory:
    def __init__(self):
        self._data: Dict[str, Thema] = themas

    def get_all(self) -> Dict[str, Thema]:
        return self._data
