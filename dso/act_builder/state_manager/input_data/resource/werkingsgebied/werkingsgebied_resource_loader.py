from typing import Optional

from ......models import PublicationSettings
from ......services.utils.helpers import load_json_data
from ......services.utils.os import create_normalized_path
from .werkingsgebied_repository import WerkingsgebiedRepository


class WerkingsgebiedResourceLoader:
    def __init__(self, base_dir: str, publication_settings: PublicationSettings, json_file_path: Optional[str]) -> None:
        self._base_dir: str = base_dir
        self._publication_settings: PublicationSettings = publication_settings
        self._json_file_path: Optional[str] = json_file_path

    def load(self) -> WerkingsgebiedRepository:
        repository = WerkingsgebiedRepository()

        if not self._json_file_path:
            return repository

        path = create_normalized_path(self._base_dir, self._json_file_path)
        loaded_json_data = load_json_data(path)
        if isinstance(loaded_json_data, dict):
            repository.add_from_dict(loaded_json_data)
        else:
            repository.add_list(load_json_data)

        return repository
