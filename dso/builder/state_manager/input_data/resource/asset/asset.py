import uuid
from enum import Enum

from pydantic import BaseModel, Field, root_validator


class IllustratieFormaat(str, Enum):
    jpg = "image/jpeg"
    jpeg = "image/jpeg"
    png = "image/png"


class IllustratieUitlijning(str, Enum):
    start = "start"
    end = "end"
    center = "center"


class Meta(BaseModel):
    Ext: str = Field(..., alias="ext")
    Breedte: int = Field(..., alias="width")
    Hoogte: int = Field(..., alias="height")
    Size: int = Field(..., alias="size")
    Formaat: IllustratieFormaat = Field(None)
    Uitlijning: IllustratieUitlijning = Field(IllustratieUitlijning.start)
    Dpi: int = Field(150)

    @root_validator(pre=True)
    def generate_formaat(fields: dict):
        fields["Formaat"] = IllustratieFormaat[fields["ext"]]
        return fields


class Asset(BaseModel):
    UUID: uuid.UUID
    Content: str
    Meta: Meta

    def get_filename(self) -> str:
        filename: str = f"img_{self.UUID}.{self.Meta.Ext}"
        return filename
