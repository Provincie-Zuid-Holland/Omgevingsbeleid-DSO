from typing import List

from ....models import ContentType
from ...services import BuilderService
from ...state_manager.input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf
from ...state_manager.input_data.resource.besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from ...state_manager.models import OutputFile, PdfContentData
from ...state_manager.state_manager import StateManager


class PdfBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        pdf_repository: BesluitPdfRepository = state_manager.input_data.resources.pdf_repository
        pdfs: List[BesluitPdf] = pdf_repository.all()

        for pdf in pdfs:
            output_file = OutputFile(
                filename=pdf.get_filename(),
                content_type=ContentType.PDF,
                content=PdfContentData(pdf=pdf),
            )
            state_manager.add_output_file(output_file)

        return state_manager
