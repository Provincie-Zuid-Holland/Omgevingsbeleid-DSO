from typing import List

from dso.act_builder.state_manager.states.text_manipulator.models import (
    TextData,
    TekstBijlageGio,
    TekstBijlageDocument,
    TekstPolicyObject,
)
from tests.factory import Factory


class TekstBijlageGioFactory(Factory):
    ids: List[int]

    def create(self) -> TekstBijlageGio:
        key = "_".join([f"gebied-{id}" for id in self.ids])
        return TekstBijlageGio(
            gio_key=key,
            eid=f"eid-tekst-bijlage-gebied-{key}",
            wid=f"wid-tekst-bijlage-gebied-{key}",
            element="a",
        )


class TekstTekstBijlageDocumentFactory(Factory):
    id: int

    def create(self) -> TekstBijlageDocument:
        return TekstBijlageDocument(
            document_code=f"document-{self.id}",
            eid=f"eid-tekst-bijlage-document-{self.id}",
            wid=f"wid-tekst-bijlage-document-{self.id}",
            element="a",
        )


class TekstPolicyObjectFactory(Factory):
    id: int

    def create(self) -> TekstPolicyObject:
        return TekstPolicyObject(
            object_code=f"beleid-{self.id}",
            eid=f"eid-tekst-policy-object-{self.id}",
            wid=f"wid-tekst-policy-object-{self.id}",
            element="a",
        )


class TextDataFactory(Factory):
    def create(self) -> TextData:
        bijlage_gebieden: List[TekstBijlageGio] = [
            TekstBijlageGioFactory(ids=[3, 4]).create(),
            TekstBijlageGioFactory(ids=[6, 7]).create(),
        ]
        bijlage_documenten: List[TekstBijlageDocument] = [
            TekstTekstBijlageDocumentFactory(id=1).create(),
            TekstTekstBijlageDocumentFactory(id=2).create(),
        ]
        policy_objects: List[TekstPolicyObject] = [
            TekstPolicyObjectFactory(id=1).create(),
            TekstPolicyObjectFactory(id=2).create(),
        ]
        return TextData(
            bijlage_gios=bijlage_gebieden,
            bijlage_documenten=bijlage_documenten,
            policy_objects=policy_objects,
        )
