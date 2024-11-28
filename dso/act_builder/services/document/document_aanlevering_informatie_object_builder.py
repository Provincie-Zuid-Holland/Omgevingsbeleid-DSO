from dso.act_builder.state_manager.input_data.resource.document.document import Document

from ....models import ContentType
from ....services.utils.hashlib import compute_sha512_of_output_file
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData
from ...state_manager.state_manager import StateManager
from .. import BuilderService


class DocumentAanleveringInformatieObjectBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        documenten = state_manager.input_data.resources.document_repository.all()

        for document in documenten:
            if document.New:
                output_file: OutputFile = self._generate_io(state_manager, document)
                state_manager.add_output_file(output_file)

        return state_manager

    def _generate_io(
        self,
        state_manager: StateManager,
        document: Document,
    ):
        document_filename = document.get_filename()
        output_file = state_manager.get_output_file_by_filename(document_filename)
        document_hash = compute_sha512_of_output_file(output_file)

        content = load_template(
            "document/AanleveringInformatieObject.xml",
            pretty_print=True,
            document_frbr=document.Frbr,
            document_filename=document_filename,
            document_hash=document_hash,
            provincie_ref=state_manager.input_data.publication_settings.provincie_ref,
            naam_informatie_object=document.Title,
        )

        output_file = OutputFile(
            filename=document.get_io_filename(),
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
