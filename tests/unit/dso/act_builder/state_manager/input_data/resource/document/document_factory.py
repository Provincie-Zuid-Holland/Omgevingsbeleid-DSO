from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.models import GioFRBR, ContentType
from tests.factory import Factory, TypeEnum


class DocumentFactory(Factory):
    id: int
    frbr: GioFRBR
    new: bool = True
    content_type: ContentType = ContentType.PDF
    geboorteregeling: str = "/akn/nl/act/pv28/2024/omgevingsvisie-1"

    def create(self) -> Document:
        title = f"Document-{id}"
        return Document(
            UUID=self.get_uuid_from_id(TypeEnum.DOCUMENT, self.id),
            Code=f"document-{id}",
            Frbr=self.frbr,
            New=self.new,
            Filename=f"document-{id}.{ContentType.PDF.lower()}",
            Title=title,
            Geboorteregeling=self.geboorteregeling,
            Content_Type=self.content_type,
            Binary=title.encode(),
        )
