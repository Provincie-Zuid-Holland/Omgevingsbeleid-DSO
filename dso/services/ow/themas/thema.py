from dso.services.ow.themas.gen import themas
from dso.services.ow.themas.types import Thema


class ThemaFactory:
    def __init__(self):
        self._data: dict[str, Thema] = themas

    def get_all(self) -> dict[str, Thema]:
        return self._data
