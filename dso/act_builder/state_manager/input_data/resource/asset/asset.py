import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator


class IllustratieFormaat(str, Enum):
    jpg = "image/jpeg"
    jpeg = "image/jpeg"  # noqa: PIE796
    png = "image/png"


class IllustratieUitlijning(str, Enum):
    start = "start"
    end = "end"
    center = "center"


class Meta(BaseModel):
    ext: str = Field(..., alias="ext")
    breedte: int = Field(..., alias="width")
    hoogte: int = Field(..., alias="height")
    size: int = Field(..., alias="size")
    formaat: IllustratieFormaat = Field(None)
    uitlijning: IllustratieUitlijning = Field(IllustratieUitlijning.start)
    dpi: int = Field(150)

    @model_validator(mode="before")
    def generate_formaat(cls, data: dict):
        if "formaat" not in data:
            data["formaat"] = IllustratieFormaat[data.get("ext", data.get("ext"))]
        return data

    model_config = ConfigDict(populate_by_name=True)


class Asset(BaseModel):
    id: uuid.UUID
    content: str
    meta: Meta

    def get_filename(self) -> str:
        filename: str = f"img_{self.id}.{self.meta.ext}"
        return filename

    @field_serializer("id")
    def serialize_uuid(cls, v: uuid.UUID) -> str:
        return str(v)

    model_config = ConfigDict(populate_by_name=True)
