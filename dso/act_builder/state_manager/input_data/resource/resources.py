from pydantic import BaseModel, ConfigDict

from dso.act_builder.state_manager.input_data.resource.document.document_repository import DocumentRepository

from .asset.asset_repository import AssetRepository
from .besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .policy_object.policy_object_repository import PolicyObjectRepository
from .werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository


class Resources(BaseModel):
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    werkingsgebied_repository: WerkingsgebiedRepository
    besluit_pdf_repository: BesluitPdfRepository
    document_repository: DocumentRepository
    model_config = ConfigDict(arbitrary_types_allowed=True)
