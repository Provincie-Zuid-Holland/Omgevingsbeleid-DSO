from pydantic import BaseModel

from .asset.asset_repository import AssetRepository
from .pdf.pdf_repository import PdfRepository
from .policy_object.policy_object_repository import PolicyObjectRepository
from .werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository


class Resources(BaseModel):
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    werkingsgebied_repository: WerkingsgebiedRepository
    pdf_repository: PdfRepository

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PolicyObjectRepository: lambda v: v.to_dict() if v is not None else None,
            AssetRepository: lambda v: v.to_dict() if v is not None else None,
            WerkingsgebiedRepository: lambda v: v.to_dict() if v is not None else None,
        }
