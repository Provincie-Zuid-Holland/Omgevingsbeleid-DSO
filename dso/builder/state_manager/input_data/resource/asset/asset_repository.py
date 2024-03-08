import uuid
from typing import Dict, List, Optional

from .asset import Asset


class AssetRepository:
    def __init__(self):
        self._assets: Dict[str, Asset] = {}

    def add(self, asset: dict):
        asset_id = asset["UUID"]
        self._assets[asset_id] = Asset.parse_obj(asset)

    def add_list(self, assets: List[dict]):
        for asset in assets:
            self.add(asset)

    def get_optional(self, idx: uuid.UUID) -> Optional[Asset]:
        asset: Optional[Asset] = self._assets.get(str(idx))
        return asset

    def get(self, idx: uuid.UUID) -> Asset:
        asset: Optional[Asset] = self.get_optional(idx)
        if asset is None:
            raise RuntimeError(f"Can not find asset {idx}")
        return asset

    def all(self) -> List[Asset]:
        return list(self._assets.values())

    def is_empty(self) -> bool:
        return not self._assets

    # def to_dict(self):
    #     return {k: v.dict() for k, v in self._assets.items()}

    def to_dict(self):
        serializable_data = {k: v.dict() for k, v in self._assets.items()}
        return serializable_data
