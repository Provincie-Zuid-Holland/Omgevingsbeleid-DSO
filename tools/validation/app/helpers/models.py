from typing import Set
from pydantic import BaseModel


class Schematron(BaseModel):
    original: str
    local: str

    def __hash__(self) -> int:
        return hash(self.original)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Schematron):
            return NotImplemented
        return self.original == other.original

    @property
    def local_file(self):
        return f"./data/schema/{self.local}"

    @property
    def step_1_file(self):
        return f"./data/tmp/{self.local}.step-1.xsl"

    @property
    def step_2_file(self):
        return f"./data/tmp/{self.local}.step-2.xsl"

    @property
    def compiled_file(self):
        return f"./data/compiled/{self.local}.xsl"

    @property
    def report_file(self):
        return f"./report/{self.local}.svrl"


class Module(BaseModel):
    file: str
    nsmap: dict


class Schemas(BaseModel):
    xsds: Set[str] = set()
    schematrons: Set[Schematron] = set()
