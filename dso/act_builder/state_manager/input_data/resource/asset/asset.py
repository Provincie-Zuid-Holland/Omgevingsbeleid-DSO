import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator


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

    @model_validator(mode="before")
    def generate_formaat(cls, values: dict):
        if "Formaat" not in values:
            values["Formaat"] = IllustratieFormaat[values.get("ext", values.get("Ext"))]
        return values

    model_config = ConfigDict(populate_by_name=True)


class Asset(BaseModel):
    UUID: uuid.UUID
    Content: str
    Meta: Meta

    def get_filename(self) -> str:
        filename: str = f"img_{self.UUID}.{self.Meta.Ext}"
        return filename

    @field_serializer("UUID")
    def serialize_uuid(cls, v: uuid.UUID) -> str:
        return str(v)

    model_config = ConfigDict(populate_by_name=True)
