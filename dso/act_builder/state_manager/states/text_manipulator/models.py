from typing import List

from pydantic import BaseModel, Field


class TekstBijlageGebied(BaseModel):
    gebied_code: str
    eid: str
    wid: str
    element: str


class TekstBijlageDocument(BaseModel):
    document_code: str
    eid: str
    wid: str
    element: str


class TekstPolicyObjectGebiedsaanwijzing(BaseModel):
    werkingsgebied_code: str
    eid: str
    wid: str
    element: str
    aanwijzing_type: str
    aanwijzing_groep: str


class TekstPolicyObject(BaseModel):
    object_code: str
    eid: str
    wid: str
    element: str
    gebiedsaanwijzingen: List[TekstPolicyObjectGebiedsaanwijzing] = Field(default_factory=list)


class TextData(BaseModel):
    bijlage_gebieden: List[TekstBijlageGebied] = Field(default_factory=list)
    bijlage_documenten: List[TekstBijlageDocument] = Field(default_factory=list)
    policy_objects: List[TekstPolicyObject] = Field(default_factory=list)

    def get_gebied_by_code(self, code: str) -> TekstBijlageGebied:
        for gebied in self.bijlage_gebieden:
            if gebied.gebied_code == code:
                return gebied
        raise RuntimeError(f"{code} not found in TextData.TekstBijlageGebied")

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
