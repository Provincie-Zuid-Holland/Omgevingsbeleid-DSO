from dataclasses import dataclass

from .asset.asset_repository import AssetRepository
from .policy_object.policy_object_repository import PolicyObjectRepository
from .werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository


@dataclass
class Resources:
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    werkingsgebied_repository: WerkingsgebiedRepository
