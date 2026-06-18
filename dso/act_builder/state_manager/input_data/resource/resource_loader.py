from .....models import PublicationSettings
from .asset.asset_resource_loader import AssetResourceLoader
from .besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .document.document_repository import DocumentRepository
from .gebieden import GebiedengroepRepository, GebiedsaanwijzingRepository, GioRepository
from .gebieden.gebiedsaanwijzing_resource_loader import GebiedsaanwijzingResourceLoader
from .gebieden.gio_resource_loader import GioResourceLoader
from .hoofdlijn.hoofdlijn_repository import HoofdlijnRepository
from .hoofdlijn.hoofdlijn_resource_loader import HoofdlijnResourceLoader
from .policy_object.policy_object_repository import PolicyObjectRepository
from .policy_object.policy_object_resource_loader import PolicyObjectResourceLoader
from .resources import Resources


class ResourceLoader:
    def __init__(self, resources_config: dict, base_dir: str, publication_settings: PublicationSettings) -> None:
        self._resources_config: dict = resources_config
        self._base_dir: str = base_dir
        self._publication_settings: PublicationSettings = publication_settings

    def load(self) -> Resources:
        asset_path = self._resources_config.get("asset_repository", None)
        asset_loader = AssetResourceLoader(
            base_dir=self._base_dir,
            json_file_path=asset_path,
        )
        asset_repository = asset_loader.load()

        gebiedsaanwijzing_path = self._resources_config.get("gebiedsaanwijzing_repository", None)
        gebiedsaanwijzing_object_loader = GebiedsaanwijzingResourceLoader(
            base_dir=self._base_dir,
            json_file_path=gebiedsaanwijzing_path,
        )
        gebiedsaanwijzingen_repository: GebiedsaanwijzingRepository = gebiedsaanwijzing_object_loader.load()

        gio_path = self._resources_config.get("gio_repository", None)
        gio_object_loader = GioResourceLoader(
            base_dir=self._base_dir,
            json_file_path=gio_path,
        )
        gio_repository: GioRepository = gio_object_loader.load()

        hoofdlijn_path = self._resources_config.get("hoofdlijn_repository", None)
        hoofdlijn_object_loader = HoofdlijnResourceLoader(
            base_dir=self._base_dir,
            json_file_path=hoofdlijn_path,
        )
        hoofdlijn_repository: HoofdlijnRepository = hoofdlijn_object_loader.load()

        policy_path = self._resources_config.get("policy_object_repository", None)
        policy_object_loader = PolicyObjectResourceLoader(
            base_dir=self._base_dir,
            json_file_path=policy_path,
        )
        policy_object_repository: PolicyObjectRepository = policy_object_loader.load()

        resources = Resources(
            policy_object_repository=policy_object_repository,
            asset_repository=asset_repository,
            gio_repository=gio_repository,
            gebiedengroep_repository=GebiedengroepRepository(),
            gebiedsaanwijzingen_repository=gebiedsaanwijzingen_repository,
            besluit_pdf_repository=BesluitPdfRepository(),
            document_repository=DocumentRepository(),
            hoofdlijn_repository=hoofdlijn_repository,
        )
        return resources
