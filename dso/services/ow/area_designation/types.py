from typing import List, Optional
from pydantic import BaseModel, Field


class AreaDesignationValue(BaseModel):
    label: str
    term: str
    uri: str
    definition: str
    explanation: str
    source: str
    domain: str
    deprecated: bool


class AreaDesignationType(BaseModel):
    label: str
    term: str
    uri: str
    definition: str
    source: str
    domain: str
    deprecated: bool


class AreaDesignationGroup(BaseModel):
    label: str
    title: str
    uri: str
    description: str
    explanation: str


class AreaDesignation(BaseModel):
    designation_type: AreaDesignationType
    designation_group: AreaDesignationGroup
    values: List[AreaDesignationValue] = Field(default_factory=list)

    def get_value_labels(self) -> List[str]:
        result: List[str] = [w.label for w in self.values]
        return result

    def get_value_by_label(self, label: str) -> Optional[AreaDesignationValue]:
        for value in self.values:
            if value.label == label:
                return value
        return None
