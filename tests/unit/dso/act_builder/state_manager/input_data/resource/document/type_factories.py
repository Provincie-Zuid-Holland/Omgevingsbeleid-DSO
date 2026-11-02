from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.models import ContentType, GioFRBR
from tests.factory import Factory, TypeEnum


class DocumentFactory(Factory):
    id: int
    frbr: GioFRBR
    new: bool = True
    content_type: ContentType = ContentType.PDF
    geboorteregeling: str = "/akn/nl/act/pv28/2024/omgevingsvisie-1"

    def create(self) -> Document:
        title = f"Document-{self.id}"
        return Document(
            id=self.get_uuid_from_id(TypeEnum.DOCUMENT, self.id),
            code=f"document-{self.id}",
            frbr=self.frbr,
            new=self.new,
            filename=f"document-{self.id}.{ContentType.PDF.lower()}",
            title=title,
            geboorteregeling=self.geboorteregeling,
            content_type=self.content_type,
            binary=title.encode(),
        )
