from pydantic import BaseModel, ConfigDict

from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedsaanwijzing_repository import GebiedsaanwijzingRepository


from .asset.asset_repository import AssetRepository
from .besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .gebieden.geogio_repository import GeoGioRepository
from .gebieden.gebied_repository import GebiedRepository
from .gebieden.gebiedengroep_repository import GebiedengroepRepository
from .policy_object.policy_object_repository import PolicyObjectRepository
from .document.document_repository import DocumentRepository


class Resources(BaseModel):
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    geogio_repository: GeoGioRepository
    gebied_repository: GebiedRepository
    gebiedengroep_repository: GebiedengroepRepository
    gebiedsaanwijzingen_repository: GebiedsaanwijzingRepository
    besluit_pdf_repository: BesluitPdfRepository
    document_repository: DocumentRepository
    model_config = ConfigDict(arbitrary_types_allowed=True)
