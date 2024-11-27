from pydantic import BaseModel

from .asset.asset_repository import AssetRepository
from .besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from .policy_object.policy_object_repository import PolicyObjectRepository
from .werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository


class Resources(BaseModel):
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    werkingsgebied_repository: WerkingsgebiedRepository
    besluit_pdf_repository: BesluitPdfRepository

    class Config:
        arbitrary_types_allowed = True
