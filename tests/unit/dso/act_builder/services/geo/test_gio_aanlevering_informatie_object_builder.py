from typing import List
from unittest.mock import MagicMock, Mock

from dso.act_builder.services.geo.gio_aanlevering_informatie_object_builder import GioAanleveringInformatieObjectBuilder
from dso.act_builder.state_manager import StateManager, StrContentData
from dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import GebiedRepository
from dso.act_builder.state_manager.input_data.resource.resources import Resources
from dso.announcement_builder.state_manager.models import InputData, OutputFile
from dso.models import PublicationSettings, ContentType
from dso.services.utils.waardelijsten import Provincie
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.type_factories import GebiedFactory
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import StateManagerTestCase
from tests.unit.dso.model_factories import GioFRBRFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestGioAanleveringInformatieObjectBuilder(StateManagerTestCase, XMLCompareTest):
    def test_apply(self):
        state_manager = MagicMock(spec=StateManager)
        state_manager.input_data = MagicMock(spec=InputData)
        state_manager.input_data.resources = MagicMock(spec=Resources)

        gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
        frbr_gebied_1 = GioFRBRFactory(Expression_Version=1).create()
        frbr_gebied_2 = GioFRBRFactory(Expression_Version=2).create()
        gebied1 = GebiedFactory(id=1, frbr=frbr_gebied_1).create()
        gebied2 = GebiedFactory(id=2, frbr=frbr_gebied_2).create()
        gebied_repository_mock.get_new.return_value = [gebied1, gebied2]
        state_manager.input_data.resources.gebied_repository = gebied_repository_mock

        state_manager.input_data.publication_settings = MagicMock(spec=PublicationSettings)
        state_manager.input_data.publication_settings.provincie_ref = Provincie.Zuid_Holland.value

        output_file_1 = self._get_output_file_mock_with_content(filename="file1.xml", content="contents file 1")
        output_file_2 = self._get_output_file_mock_with_content(filename="file2.xml", content="contents file 2")
        state_manager.get_output_file_by_filename.side_effect = [output_file_1, output_file_2]

        builder = GioAanleveringInformatieObjectBuilder()
        builder.apply(state_manager)

        output_files: List[OutputFile] = self._get_output_files(state_manager)
        assert len(output_files) == 2

        for idx, output_file in enumerate(output_files):
            with open(self._get_xml_file_path(__file__, idx), "r") as f:
                expected = f.read()
                assert output_file.content.content == expected

    def _get_output_file_mock_with_content(self, filename: str, content: str):
        output_file: OutputFile = OutputFile(
            filename=filename,
            content_type=ContentType.XML,
            content=StrContentData(content=content),
        )
        return output_file
