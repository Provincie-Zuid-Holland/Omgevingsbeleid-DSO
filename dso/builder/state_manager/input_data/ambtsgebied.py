from pydantic import BaseModel


class Ambtsgebied(BaseModel):
    identificatie_suffix: str
    domein: str
    geldig_op: str
    new: bool
