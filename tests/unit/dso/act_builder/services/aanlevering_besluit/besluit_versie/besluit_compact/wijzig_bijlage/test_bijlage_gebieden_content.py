from unittest.mock import MagicMock

from dso.act_builder.services.aanlevering_besluit.besluit_versie.besluit_compact.wijzig_bijlage.bijlage_gebieden_content import (
    BijlageGebiedenContent,
)
from dso.act_builder.state_manager import StateManager
from dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import GebiedRepository
from dso.act_builder.state_manager.input_data.resource.resources import Resources
from dso.announcement_builder.state_manager.models import InputData
from dso.services.ewid.ewid_service import EWIDService
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.type_factories import GebiedFactory
from tests.unit.dso.model_factories import GioFRBRFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestBijlageGebiedenContent(XMLCompareTest):
    def test_create(self) -> None:
        state_manager = MagicMock(spec=StateManager)
        state_manager.input_data = MagicMock(spec=InputData)
        state_manager.input_data.resources = MagicMock(spec=Resources)

        gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
        gio_gebied = GioFRBRFactory().create()
        gebied1 = GebiedFactory(id=1, title="gebied 1", code="gebied-1", frbr=gio_gebied).create()
        gebied2 = GebiedFactory(id=2, title="gebied 2", code="gebied-2", frbr=gio_gebied).create()
        gebied_repository_mock.all.return_value = [gebied1, gebied2]
        state_manager.input_data.resources.gebied_repository = gebied_repository_mock

        act_ewid_service = EWIDService(wid_prefix="pv28")
        state_manager.act_ewid_service = act_ewid_service

        bijlage_gebieden_content = BijlageGebiedenContent(state_manager)
        actual = bijlage_gebieden_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected
