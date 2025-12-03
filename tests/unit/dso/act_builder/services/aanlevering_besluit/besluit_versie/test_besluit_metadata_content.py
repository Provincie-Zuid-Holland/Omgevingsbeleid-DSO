from unittest.mock import MagicMock

from dso.act_builder.services.aanlevering_besluit.besluit_versie.besluit_metadata_content import BesluitMetadataContent
from dso.act_builder.state_manager import StateManager
from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf
from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from dso.act_builder.state_manager.input_data.resource.document.document import Document
from dso.act_builder.state_manager.input_data.resource.document.document_repository import DocumentRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import GebiedRepository
from dso.act_builder.state_manager.input_data.resource.resources import Resources
from dso.announcement_builder.state_manager.models import InputData
from dso.models import PublicationSettings
from dso.services.utils.waardelijsten import Provincie, BestuursorgaanSoort
from tests.unit.dso.act_builder.state_manager.input_data.besluit_factories import BesluitFactory
from tests.unit.dso.act_builder.state_manager.input_data.regeling_factories import RegelingFactory
from tests.unit.dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf_factory import (
    BesluitPdfFactory,
)
from tests.unit.dso.act_builder.state_manager.input_data.resource.document.document_factory import DocumentFactory
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.type_factories import GebiedFactory
from tests.unit.dso.model_factories import GioFRBRFactory, PubdataFRBRFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestBesluitMetadataContent(XMLCompareTest):
    def test_create(self) -> None:
        state_manager = MagicMock(spec=StateManager)
        state_manager.input_data = MagicMock(spec=InputData)
        state_manager.input_data.resources = MagicMock(spec=Resources)
        state_manager.input_data.publication_settings = MagicMock(spec=PublicationSettings)

        gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
        frbr_gebied_1 = GioFRBRFactory(Expression_Version=1).create()
        frbr_gebied_2 = GioFRBRFactory(Expression_Version=2).create()
        gebied1 = GebiedFactory(id=1, frbr=frbr_gebied_1).create()
        gebied2 = GebiedFactory(id=2, frbr=frbr_gebied_2).create()
        gebied_repository_mock.get_new.return_value = [gebied1, gebied2]
        state_manager.input_data.resources.gebied_repository = gebied_repository_mock

        document_repository_mock: DocumentRepository | MagicMock = MagicMock(spec=DocumentRepository)
        frbr_document_1 = GioFRBRFactory(Expression_Version=3).create()
        document_1: Document = DocumentFactory(id=1, frbr=frbr_document_1).create()
        document_repository_mock.all.return_value = [document_1]
        state_manager.input_data.resources.document_repository = document_repository_mock

        besluit_pdf_repository_mock: BesluitPdfRepository | MagicMock = MagicMock(spec=BesluitPdfRepository)
        frbr_besluit_pdf_1 = PubdataFRBRFactory(Expression_Version=1).create()
        besluit_pdf_1: BesluitPdf = BesluitPdfFactory(id=1, frbr=frbr_besluit_pdf_1).create()
        besluit_pdf_repository_mock.all.return_value = [besluit_pdf_1]
        state_manager.input_data.resources.besluit_pdf_repository = besluit_pdf_repository_mock

        besluit_factory = BesluitFactory()
        state_manager.input_data.besluit = besluit_factory.create()

        regeling_factory = RegelingFactory()
        state_manager.input_data.regeling = regeling_factory.create()

        state_manager.input_data.publication_settings.provincie_ref = Provincie.Zuid_Holland.value
        state_manager.input_data.publication_settings.soort_bestuursorgaan = BestuursorgaanSoort.Provinciale_staten

        besluit_metadata_content = BesluitMetadataContent(state_manager)
        actual = besluit_metadata_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected
