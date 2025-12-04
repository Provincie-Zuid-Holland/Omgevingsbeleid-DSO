from dso.act_builder.services.aanlevering_besluit.besluit_versie.besluit_compact.wijzig_bijlage.bijlage_gebieden_content import (
    BijlageGebiedenContent,
)
from dso.services.ewid.ewid_service import EWIDService
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import (
    gebied_repository_mock_with_two_gebieden,
    gebied_repository_mock_empty,
)
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import state_manager_mock
from tests.unit.xml_compare_test import XMLCompareTest


class TestBijlageGebiedenContent(XMLCompareTest):
    def test_create(self, state_manager_mock, gebied_repository_mock_with_two_gebieden) -> None:
        state_manager_mock.input_data.resources.gebied_repository = gebied_repository_mock_with_two_gebieden

        act_ewid_service = EWIDService(wid_prefix="pv28")
        state_manager_mock.act_ewid_service = act_ewid_service

        bijlage_gebieden_content = BijlageGebiedenContent(state_manager_mock)
        actual = bijlage_gebieden_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected

    def test_create_no_gebieden(self, state_manager_mock, gebied_repository_mock_empty) -> None:
        state_manager_mock.input_data.resources.gebied_repository = gebied_repository_mock_empty

        bijlage_gebieden_content = BijlageGebiedenContent(state_manager_mock)
        actual = bijlage_gebieden_content.create()
        assert actual == ""
