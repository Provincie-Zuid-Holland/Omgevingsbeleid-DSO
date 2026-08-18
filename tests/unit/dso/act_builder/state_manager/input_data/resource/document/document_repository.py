from unittest.mock import MagicMock, Mock

import pytest

from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.act_builder.state_manager.input_data.resource.document.document_repository import DocumentRepository
from tests.unit.dso.act_builder.state_manager.input_data.resource.document.type_factories import DocumentFactory
from tests.unit.dso.model_factories import FRBRType, GioFRBRFactory


@pytest.fixture
def document_repository_mock_with_two_new_documents() -> DocumentRepository | Mock:
    document_repository_mock: DocumentRepository | MagicMock = MagicMock(spec=DocumentRepository)
    document_repository_mock.get_new.return_value = _get_documents()
    return document_repository_mock


@pytest.fixture
def document_repository_mock_with_two_documents() -> DocumentRepository | Mock:
    document_repository_mock: DocumentRepository | MagicMock = MagicMock(spec=DocumentRepository)
    document_repository_mock.all.return_value = _get_documents()
    return document_repository_mock


def _get_documents(count: int = 2) -> list[Document | Mock]:
    documents: list[Document | Mock] = []
    for i in range(1, count + 1):
        frbr = GioFRBRFactory(frbr_type=FRBRType.DOCUMENT, Expression_Version=i).create()
        document = DocumentFactory(id=i, frbr=frbr).create()
        documents.append(document)
    return documents


@pytest.fixture
def document_repository_mock_empty() -> DocumentRepository | Mock:
    document_repository_mock: DocumentRepository | MagicMock = MagicMock(spec=DocumentRepository)
    document_repository_mock.get_new.return_value = []
    return document_repository_mock
