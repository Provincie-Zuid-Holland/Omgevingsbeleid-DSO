import json
import uuid

from .asset import Asset


class AssetRepository:
    def __init__(self):
        self._assets: dict[str, Asset] = {}

    def add(self, asset: dict):
        asset_id = asset["UUID"]
        self._assets[asset_id] = Asset.model_validate(asset)

    def add_list(self, assets: list[dict]):
        for asset in assets:
            self.add(asset)

    def add_from_dict(self, assets: dict[str, dict]) -> None:
        for asset in assets.values():
            self.add(asset)

    def get_optional(self, idx: uuid.UUID) -> Asset | None:
        asset: Asset | None = self._assets.get(str(idx))
        return asset

    def get(self, idx: uuid.UUID) -> Asset:
        asset: Asset | None = self.get_optional(idx)
        if asset is None:
            raise RuntimeError(f"Can not find asset {idx}")
        return asset

    def all(self) -> list[Asset]:
        return list(self._assets.values())

    def is_empty(self) -> bool:
        return not self._assets

    def to_dict(self):
        return {str(k): json.loads(v.model_dump_json()) for k, v in self._assets.items()}
