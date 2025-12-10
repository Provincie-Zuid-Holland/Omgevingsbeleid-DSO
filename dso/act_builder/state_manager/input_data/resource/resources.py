from pydantic import BaseModel, ConfigDict

from dso.act_builder.state_manager.input_data.resource.document.document_repository import DocumentRepository

from .asset.asset_repository import AssetRepository
from .besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .gebieden.gebied_repository import GebiedRepository
from .gebieden.gebiedengroep_repository import GebiedengroepRepository
from .policy_object.policy_object_repository import PolicyObjectRepository


class Resources(BaseModel):
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    gebied_repository: GebiedRepository
    gebiedengroep_repository: GebiedengroepRepository
    besluit_pdf_repository: BesluitPdfRepository
    document_repository: DocumentRepository
    model_config = ConfigDict(arbitrary_types_allowed=True)
