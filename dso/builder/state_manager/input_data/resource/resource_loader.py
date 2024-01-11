from .asset.asset_resource_loader import AssetResourceLoader
from .policy_object.policy_object_resource_loader import (
    PolicyObjectResourceLoader,
)
from .werkingsgebied.werkingsgebied_resource_loader import (
    WerkingsgebiedResourceLoader,
)
from .....models import PublicationSettings

from .resources import Resources


class ResourceLoader:
    def __init__(self, resources_config: dict, base_dir: str, publication_settings: PublicationSettings):
        self._resources_config: dict = resources_config
        self._base_dir: str = base_dir
        self._publication_settings: PublicationSettings = publication_settings

    def load(self) -> Resources:
        policy_object_loader = PolicyObjectResourceLoader(
            self._base_dir,
            self._resources_config.get("policy-objects", []),
        )
        policy_object_repository = policy_object_loader.load()

        werkingsgebied_loader = WerkingsgebiedResourceLoader(
            self._base_dir,
            self._publication_settings,
            self._resources_config.get("werkingsgebieden", []),
        )
        werkingsgebied_repository = werkingsgebied_loader.load()

        asset_loader = AssetResourceLoader(
            self._base_dir,
            self._resources_config.get("assets", []),
        )
        asset_repository = asset_loader.load()

        resources = Resources(
            policy_object_repository=policy_object_repository,
            asset_repository=asset_repository,
            werkingsgebied_repository=werkingsgebied_repository,
        )
        return resources
