from typing import List

from dso.act_builder.services.geo.geo_informatie_object_vaststelling_builder import (
    GeoInformatieObjectVaststellingBuilder,
)
from dso.announcement_builder.state_manager.models import OutputFile
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import (
    gio_repository_mock_with_two_new_gebieden,
)
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import StateManagerTestCase, state_manager_mock
from tests.unit.xml_compare_test import XMLCompareTest


class TestGeoInformatieObjectVaststellingBuilder(StateManagerTestCase, XMLCompareTest):
    def test_apply(self, state_manager_mock, gio_repository_mock_with_two_new_gebieden):
        state_manager_mock.input_data.resources.gio_repository = gio_repository_mock_with_two_new_gebieden

        builder = GeoInformatieObjectVaststellingBuilder()
        builder.apply(state_manager_mock)

        output_files: List[OutputFile] = self._get_output_files(state_manager_mock)
        assert len(output_files) == 2

        for idx, output_file in enumerate(output_files):
            with open(self._get_xml_file_path(__file__, idx), "r") as f:
                expected = f.read()
                assert output_file.content.content == expected
