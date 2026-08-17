from pydantic import BaseModel, ConfigDict

from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedsaanwijzing_repository import (
    GebiedsaanwijzingRepository,
)

from .asset.asset_repository import AssetRepository
from .besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .document.document_repository import DocumentRepository
from .gebieden.gebiedengroep_repository import GebiedengroepRepository
from .gebieden.gio_repository import GioRepository
from .policy_object.policy_object_repository import PolicyObjectRepository


class Resources(BaseModel):
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    gio_repository: GioRepository
    gebiedengroep_repository: GebiedengroepRepository
    gebiedsaanwijzingen_repository: GebiedsaanwijzingRepository
    besluit_pdf_repository: BesluitPdfRepository
    document_repository: DocumentRepository
    model_config = ConfigDict(arbitrary_types_allowed=True)
