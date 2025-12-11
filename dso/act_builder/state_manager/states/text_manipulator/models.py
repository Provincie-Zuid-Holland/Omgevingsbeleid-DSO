from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class TekstBijlageGio(BaseModel):
    gio_key: str
    eid: str
    wid: str
    element: str


class TekstBijlageDocument(BaseModel):
    document_code: str
    eid: str
    wid: str
    element: str


class TekstPolicyObjectGebiedsaanwijzing(BaseModel):
    uuid: UUID
    eid: str
    wid: str
    element: str


class TekstPolicyObject(BaseModel):
    object_code: str
    eid: str
    wid: str
    element: str
    gebiedsaanwijzingen: List[TekstPolicyObjectGebiedsaanwijzing] = Field(default_factory=list)


class TextData(BaseModel):
    bijlage_gios: List[TekstBijlageGio] = Field(default_factory=list)
    bijlage_documenten: List[TekstBijlageDocument] = Field(default_factory=list)
    policy_objects: List[TekstPolicyObject] = Field(default_factory=list)

    def get_gio_by_key(self, gio_key: str) -> TekstBijlageGio:
        for gio in self.bijlage_gios:
            if gio.gio_key == gio_key:
                return gio
        raise RuntimeError(f"{gio_key} not found in TextData.TekstBijlageGio")

    def get_document_by_code(self, code: str) -> TekstBijlageDocument:
        for document in self.bijlage_documenten:
            if document.document_code == code:
                return document
        raise RuntimeError(f"{code} not found in TextData.TekstBijlageDocument")

    def get_policy_object_by_code(self, code: str) -> TekstPolicyObject:
        for policy_object in self.policy_objects:
            if policy_object.object_code == code:
                return policy_object
        raise RuntimeError(f"{code} not found in TextData.TekstPolicyObject")
