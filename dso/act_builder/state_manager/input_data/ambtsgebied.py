import uuid

from pydantic import BaseModel


class Ambtsgebied(BaseModel):
    UUID: uuid.UUID
    identificatie_suffix: str
    domein: str
    geldig_op: str
    titel: str

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
