import json
import uuid
from typing import Dict, List, Optional

from .asset import Asset


class AssetRepository:
    def __init__(self):
        self._assets: Dict[str, Asset] = {}

    def add(self, asset: dict):
        asset_id = asset["UUID"]
        self._assets[asset_id] = Asset.model_validate(asset)

    def add_list(self, assets: List[dict]):
        for asset in assets:
            self.add(asset)

    def add_from_dict(self, assets: Dict[str, dict]) -> None:
        for asset_uuid, asset in assets.items():
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

    def to_dict(self):
        return {str(k): json.loads(v.json()) for k, v in self._assets.items()}
