from typing import List

from ....models import ContentType
from ....services.utils.hashlib import compute_sha512_of_output_file
from ....services.utils.helpers import load_template
from ...services import BuilderService
from ...state_manager.input_data.resource.pdf.pdf import Pdf
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager


class PdfAanleveringInformatieObjectBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        pdfs: List[Pdf] = state_manager.input_data.resources.pdf_repository.all()

        for pdf in pdfs:
            output_file: OutputFile = self._generate_io(state_manager, pdf)
            state_manager.add_output_file(output_file)

        return state_manager

    def _generate_io(
        self,
        state_manager: StateManager,
        pdf: Pdf,
    ):
        pdf_filename = pdf.get_filename()
        output_file = state_manager.get_output_file_by_filename(pdf_filename)
        pdf_hash = compute_sha512_of_output_file(output_file)

        content = load_template(
            "pdf/AanleveringInformatieObject.xml",
            pretty_print=True,
            pdf_frbr=pdf.frbr,
            pdf_filename=pdf_filename,
            pdf_hash=pdf_hash,
            provincie_ref=state_manager.input_data.publication_settings.provincie_ref,
            naam_informatie_object=pdf.title,
        )

        output_file = OutputFile(
            filename=pdf.get_io_filename(),
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
