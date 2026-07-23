from dso.act_builder.services.aanlevering_besluit.besluit_versie.besluit_compact.artikelen_content import (
    ArtikelenContent,
)
from tests.unit.dso.act_builder.state_manager.input_data.besluit_factories import BesluitFactory
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import state_manager_mock
from tests.unit.dso.act_builder.state_manager.states.artikel_eid_repository import artikel_eid_repository_with_eid_data
from tests.unit.dso.model_factories import ActFRBRFactory
from tests.unit.xml_compare_test import XMLCompareTest


class TestArtikelenContent(XMLCompareTest):
    def test_create(
        self,
        state_manager_mock,
        artikel_eid_repository_with_eid_data,
    ) -> None:
        state_manager_mock.input_data.publication_settings.provincie_id = "pv28"
        state_manager_mock.input_data.publication_settings.regeling_frbr = ActFRBRFactory(Expression_Version=1).create()

        state_manager_mock.artikel_eid = artikel_eid_repository_with_eid_data

        besluit_factory = BesluitFactory()
        state_manager_mock.input_data.besluit = besluit_factory.create()

        artikelen_content = ArtikelenContent(state_manager_mock)
        actual = artikelen_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected
