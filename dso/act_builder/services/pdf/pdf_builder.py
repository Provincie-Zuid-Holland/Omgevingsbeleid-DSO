from typing import List

from ...services import BuilderService
from ...state_manager.input_data.resource.pdf.pdf import Pdf
from ...state_manager.input_data.resource.pdf.pdf_repository import PdfRepository
from ...state_manager.models import PdfContentData, OutputFile
from ...state_manager.state_manager import StateManager
from ....models import ContentType


class PdfBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        pdf_repository: PdfRepository = state_manager.input_data.resources.pdf_repository
        pdfs: List[Pdf] = pdf_repository.all()

        for pdf in pdfs:
            output_file = OutputFile(
                filename=pdf.get_filename(),
                content_type=ContentType.PDF,
                content=PdfContentData(pdf=pdf),
            )
            state_manager.add_output_file(output_file)

        return state_manager
