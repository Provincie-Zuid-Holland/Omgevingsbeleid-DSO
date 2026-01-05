from unittest.mock import MagicMock

from dso.act_builder.services.aanlevering_besluit.besluit_versie.besluit_metadata_content import BesluitMetadataContent
from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf import BesluitPdf
from dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf_repository import BesluitPdfRepository
from dso.services.utils.waardelijsten import Provincie, BestuursorgaanSoort
from tests.unit.dso.act_builder.state_manager.input_data.besluit_factories import BesluitFactory
from tests.unit.dso.act_builder.state_manager.input_data.regeling_factories import RegelingFactory
from tests.unit.dso.act_builder.state_manager.input_data.resource.besluit_pdf.besluit_pdf_factory import (
    BesluitPdfFactory,
)
from tests.unit.dso.act_builder.state_manager.input_data.resource.document.document_repository import (
    document_repository_mock_with_two_documents,
)
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import (
    gio_repository_mock_with_two_new_gebieden,
)
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import state_manager_mock
from tests.unit.dso.model_factories import PubdataFRBRFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestBesluitMetadataContent(XMLCompareTest):
    def test_create(
        self,
        state_manager_mock,
        gio_repository_mock_with_two_new_gebieden,
        document_repository_mock_with_two_documents,
    ) -> None:
        state_manager_mock.input_data.resources.gio_repository = gio_repository_mock_with_two_new_gebieden

        state_manager_mock.input_data.resources.document_repository = document_repository_mock_with_two_documents

        besluit_pdf_repository_mock: BesluitPdfRepository | MagicMock = MagicMock(spec=BesluitPdfRepository)
        frbr_besluit_pdf_1 = PubdataFRBRFactory(Expression_Version=1).create()
        besluit_pdf_1: BesluitPdf = BesluitPdfFactory(id=1, frbr=frbr_besluit_pdf_1).create()
        besluit_pdf_repository_mock.all.return_value = [besluit_pdf_1]
        state_manager_mock.input_data.resources.besluit_pdf_repository = besluit_pdf_repository_mock

        besluit_factory = BesluitFactory()
        state_manager_mock.input_data.besluit = besluit_factory.create()

        regeling_factory = RegelingFactory()
        state_manager_mock.input_data.regeling = regeling_factory.create()

        state_manager_mock.input_data.publication_settings.provincie_ref = Provincie.Zuid_Holland.value
        state_manager_mock.input_data.publication_settings.soort_bestuursorgaan = BestuursorgaanSoort.Provinciale_staten

        besluit_metadata_content = BesluitMetadataContent(state_manager_mock)
        actual = besluit_metadata_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected
