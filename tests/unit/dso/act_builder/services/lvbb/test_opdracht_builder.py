from unittest.mock import MagicMock

from dso.act_builder.services.lvbb.opdracht_builder import OpdrachtBuilder
from dso.act_builder.state_manager import OutputFile, StateManager
from dso.act_builder.state_manager.input_data.input_data_loader import InputData
from dso.models import PublicationSettings, PublicatieOpdracht, OpdrachtType
from tests.unit.dso.act_builder.state_manager_test_case import StateManagerTestCase


class TestOpdrachtBuilder(StateManagerTestCase):
    def test_apply(self):
        state_manager = MagicMock(spec=StateManager)
        state_manager.input_data = MagicMock(spec=InputData)
        state_manager.input_data.publication_settings = MagicMock(spec=PublicationSettings)

        opdracht = PublicatieOpdracht(
            id_levering="id-levering",
            opdracht_type=OpdrachtType.PUBLICATIE,
            id_bevoegdgezag="id-bevoegdgezag67890",
            publicatie_bestand="akn_publicatie_bestand_v1",
            datum_bekendmaking="2025-11-25",
        )
        state_manager.input_data.publication_settings.opdracht = opdracht

        opdracht_builder = OpdrachtBuilder()
        opdracht_builder.apply(state_manager)

        expected_xml = """<?xml version='1.0' encoding='utf-8'?>
<publicatieOpdracht xmlns="http://www.overheid.nl/2017/lvbb">
  <idLevering>id-levering</idLevering>
  <idBevoegdGezag>id-bevoegdgezag67890</idBevoegdGezag>
  <idAanleveraar>00000003011411800000</idAanleveraar>
  <publicatie>akn_publicatie_bestand_v1</publicatie>
  <datumBekendmaking>2025-11-25</datumBekendmaking>
</publicatieOpdracht>
"""

        output_file: OutputFile = self._get_output_file(state_manager)
        assert self._normalize_xml(output_file.content.content) == self._normalize_xml(expected_xml)
