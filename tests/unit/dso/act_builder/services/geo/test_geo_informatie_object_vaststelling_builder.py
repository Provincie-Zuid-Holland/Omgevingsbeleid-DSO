from typing import List
from unittest.mock import MagicMock

from dso.act_builder.services.geo.geo_informatie_object_vaststelling_builder import (
    GeoInformatieObjectVaststellingBuilder,
)
from dso.act_builder.state_manager import StateManager
from dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import GebiedRepository
from dso.act_builder.state_manager.input_data.resource.resources import Resources
from dso.announcement_builder.state_manager.models import InputData, OutputFile
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.type_factories import GebiedFactory
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import StateManagerTestCase
from tests.unit.dso.model_factories import GioFRBRFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestGeoInformatieObjectVaststellingBuilder(StateManagerTestCase, XMLCompareTest):
    def test_apply(self):
        state_manager = MagicMock(spec=StateManager)
        state_manager.input_data = MagicMock(spec=InputData)
        state_manager.input_data.resources = MagicMock(spec=Resources)

        gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
        frbr_gebied_1 = GioFRBRFactory(Expression_Version=1).create()
        frbr_gebied_2 = GioFRBRFactory(Expression_Version=2).create()
        gebied1 = GebiedFactory(id=1, gml="<gml:Point/>", frbr=frbr_gebied_1).create()
        gebied2 = GebiedFactory(id=2, gml="<gml:Point/>", frbr=frbr_gebied_2).create()
        gebied_repository_mock.get_new.return_value = [gebied1, gebied2]
        state_manager.input_data.resources.gebied_repository = gebied_repository_mock

        builder = GeoInformatieObjectVaststellingBuilder()
        builder.apply(state_manager)

        output_files: List[OutputFile] = self._get_output_files(state_manager)
        assert len(output_files) == 2

        for idx, output_file in enumerate(output_files):
            with open(self._get_xml_file_path(__file__, idx), "r") as f:
                expected = f.read()
                assert output_file.content.content == expected
