import uuid

from pydantic import BaseModel


class Ambtsgebied(BaseModel):
    UUID: uuid.UUID
    identificatie_suffix: str
    domein: str
    geldig_op: str
    new: bool
