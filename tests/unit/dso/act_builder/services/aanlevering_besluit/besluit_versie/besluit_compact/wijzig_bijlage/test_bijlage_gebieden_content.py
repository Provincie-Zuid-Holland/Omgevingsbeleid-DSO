from dso.act_builder.services.aanlevering_besluit.besluit_versie.besluit_compact.wijzig_bijlage.bijlage_gios_content import (
    BijlageGioContent,
)
from dso.services.ewid.ewid_service import EWIDService
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import (
    gio_repository_mock_with_two_gebieden,
    gio_repository_mock_empty,
)
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import state_manager_mock
from tests.unit.dso.act_builder.state_manager.states.text_manipulator.model_factories import TextDataFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestBijlageGioContent(XMLCompareTest):
    def test_create(self, state_manager_mock, gio_repository_mock_with_two_gebieden) -> None:
        state_manager_mock.input_data.resources.gio_repository = gio_repository_mock_with_two_gebieden

        act_ewid_service = EWIDService(wid_prefix="pv28")
        state_manager_mock.act_ewid_service = act_ewid_service

        state_manager_mock.text_data = TextDataFactory().create()

        bijlage_gio_content = BijlageGioContent(state_manager_mock)
        actual = bijlage_gio_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected

    def test_create_no_gios(self, state_manager_mock, gio_repository_mock_empty) -> None:
        state_manager_mock.input_data.resources.gio_repository = gio_repository_mock_empty

        bijlage_gio_content = BijlageGioContent(state_manager_mock)
        actual = bijlage_gio_content.create()
        assert actual == ""
