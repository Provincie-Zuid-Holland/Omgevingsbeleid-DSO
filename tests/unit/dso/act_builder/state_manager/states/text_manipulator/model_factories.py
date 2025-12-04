from dso.act_builder.state_manager.states.text_manipulator.models import (
    TextData,
    TekstBijlageGebied,
    TekstBijlageDocument,
    TekstPolicyObject,
)
from tests.factory import Factory


class TekstBijlageGebiedFactory(Factory):
    id: int

    def create(self) -> TekstBijlageGebied:
        return TekstBijlageGebied(
            gebied_code=f"gebied-{self.id}",
            eid=f"eid-tekst-bijlage-gebied-{self.id}",
            wid=f"wid-tekst-bijlage-gebied-{self.id}",
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
        bijlage_gebieden = [
            TekstBijlageGebiedFactory(id=1).create(),
            TekstBijlageGebiedFactory(id=2).create(),
        ]
        bijlage_documenten = [
            TekstTekstBijlageDocumentFactory(id=1).create(),
            TekstTekstBijlageDocumentFactory(id=2).create(),
        ]
        policy_objects = [
            TekstPolicyObjectFactory(id=1).create(),
            TekstPolicyObjectFactory(id=2).create(),
        ]
        return TextData(
            bijlage_gebieden=bijlage_gebieden,
            bijlage_documenten=bijlage_documenten,
            policy_objects=policy_objects,
        )
