from typing import List

from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.act_builder.state_manager.input_data.resource.document.document_repository import DocumentRepository

from ...builder_service import BuilderService
from ...state_manager.models import DocumentContentData, OutputFile
from ...state_manager.state_manager import StateManager


class DocumentBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        document_repository: DocumentRepository = state_manager.input_data.resources.document_repository
        documents: List[Document] = document_repository.all()

        for document in documents:
            if document.New:
                output_file = OutputFile(
                    filename=document.get_filename(),
                    content_type=document.Content_Type,
                    content=DocumentContentData(document=document),
                )
                state_manager.add_output_file(output_file)

        return state_manager
