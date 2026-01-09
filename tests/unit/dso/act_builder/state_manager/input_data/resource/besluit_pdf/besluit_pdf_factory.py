from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf
from dso.models import PubdataFRBR
from tests.factory import Factory, TypeEnum


class BesluitPdfFactory(Factory):
    id: int
    frbr: PubdataFRBR

    def create(self) -> BesluitPdf:
        title = f"Besluit PDF {self.id}"
        return BesluitPdf(
            id=self.id,
            uuid=self.get_uuid_from_id(TypeEnum.BESLUIT_PDF, self.id),
            filename=f"besluit-pdf-{id}",
            title=title,
            binary=title.encode(),
            frbr=self.frbr,
        )
