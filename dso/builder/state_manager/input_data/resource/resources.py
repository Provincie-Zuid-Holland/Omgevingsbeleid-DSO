from dataclasses import dataclass

from dso.builder.state_manager.input_data.resource.asset.asset_repository import AssetRepository
from dso.builder.state_manager.input_data.resource.policy_object.policy_object_repository import PolicyObjectRepository
from dso.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)


@dataclass
class Resources:
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    werkingsgebied_repository: WerkingsgebiedRepository
