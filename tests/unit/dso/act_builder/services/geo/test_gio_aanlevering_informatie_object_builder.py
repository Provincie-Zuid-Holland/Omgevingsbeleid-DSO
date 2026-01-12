from typing import List

from dso.act_builder.services.geo.gio_aanlevering_informatie_object_builder import GioAanleveringInformatieObjectBuilder
from dso.act_builder.state_manager import StrContentData
from dso.announcement_builder.state_manager.models import OutputFile
from dso.models import ContentType
from dso.services.utils.waardelijsten import Provincie
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import (
    gio_repository_mock_with_two_new_gebieden,
)
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import StateManagerTestCase, state_manager_mock
from tests.unit.xml_compare_test import XMLCompareTest


class TestGioAanleveringInformatieObjectBuilder(StateManagerTestCase, XMLCompareTest):
    def test_apply(self, state_manager_mock, gio_repository_mock_with_two_new_gebieden):
        state_manager_mock.input_data.resources.gio_repository = gio_repository_mock_with_two_new_gebieden

        state_manager_mock.input_data.publication_settings.provincie_ref = Provincie.Zuid_Holland.value

        output_file_1 = self._get_output_file_mock_with_content(filename="file1.xml", content="contents file 1")
        output_file_2 = self._get_output_file_mock_with_content(filename="file2.xml", content="contents file 2")
        state_manager_mock.get_output_file_by_filename.side_effect = [output_file_1, output_file_2]

        builder = GioAanleveringInformatieObjectBuilder()
        builder.apply(state_manager_mock)

        output_files: List[OutputFile] = self._get_output_files(state_manager_mock)
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
