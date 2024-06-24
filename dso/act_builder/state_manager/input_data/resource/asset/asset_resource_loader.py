from typing import Optional

from ......services.utils.helpers import load_json_data
from ......services.utils.os import create_normalized_path
from .asset_repository import AssetRepository


class AssetResourceLoader:
    def __init__(self, base_dir: str, json_file_path: Optional[str]) -> None:
        self._base_dir: str = base_dir
        self._json_file_path: Optional[str] = json_file_path

    def load(self) -> AssetRepository:
        repository = AssetRepository()

        if not self._json_file_path:
            return repository

        path = create_normalized_path(self._base_dir, self._json_file_path)
        loaded_json_data = load_json_data(path)
        repository.add_from_dict(loaded_json_data)

        return repository
