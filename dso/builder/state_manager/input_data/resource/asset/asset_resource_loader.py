from typing import List

from .asset_repository import AssetRepository
from ......services.utils.helpers import load_json_data
from ......services.utils.os import create_normalized_path


class AssetResourceLoader:
    def __init__(self, base_dir: str, asset_files: List[str]):
        self._base_dir: str = base_dir
        self._asset_files: List[str] = asset_files

    def load(self) -> AssetRepository:
        repository = AssetRepository()

        for asset_file in self._asset_files:
            path = create_normalized_path(self._base_dir, asset_file)
            asset = load_json_data(path)
            if isinstance(asset, dict):
                repository.add(asset)
            else:
                repository.add_list(asset)

        return repository
