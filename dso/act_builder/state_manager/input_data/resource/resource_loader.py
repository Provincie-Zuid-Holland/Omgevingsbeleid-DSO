from .....models import PublicationSettings
from .asset.asset_resource_loader import AssetResourceLoader
from .pdf.pdf_repository import PdfRepository
from .policy_object.policy_object_resource_loader import PolicyObjectResourceLoader
from .resources import Resources
from .werkingsgebied.werkingsgebied_resource_loader import WerkingsgebiedResourceLoader


class ResourceLoader:
    def __init__(self, resources_config: dict, base_dir: str, publication_settings: PublicationSettings) -> None:
        self._resources_config: dict = resources_config
        self._base_dir: str = base_dir
        self._publication_settings: PublicationSettings = publication_settings

    def load(self) -> Resources:
        policy_path = self._resources_config.get("policy_object_repository", None)
        policy_object_loader = PolicyObjectResourceLoader(
            base_dir=self._base_dir,
            json_file_path=policy_path,
        )
        policy_object_repository = policy_object_loader.load()

        werkingsgebied_path = self._resources_config.get("werkingsgebied_repository", None)
        werkingsgebied_loader = WerkingsgebiedResourceLoader(
            base_dir=self._base_dir,
            publication_settings=self._publication_settings,
            json_file_path=werkingsgebied_path,
        )
        werkingsgebied_repository = werkingsgebied_loader.load()

        asset_path = self._resources_config.get("asset_repository", None)
        asset_loader = AssetResourceLoader(
            base_dir=self._base_dir,
            json_file_path=asset_path,
        )
        asset_repository = asset_loader.load()

        resources = Resources(
            policy_object_repository=policy_object_repository,
            asset_repository=asset_repository,
            werkingsgebied_repository=werkingsgebied_repository,
            pdf_repository=PdfRepository(),
        )
        return resources
