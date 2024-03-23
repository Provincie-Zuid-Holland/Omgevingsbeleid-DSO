from typing import List

from lxml import etree

from .......models import PublicationSettings
from .......services.ewid.ewid_service import EWIDService
from .......services.utils.helpers import load_template
from ......state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ......state_manager.state_manager import StateManager


class BijlageWerkingsgebiedenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        all_werkingsgebieden: List[Werkingsgebied] = (
            self._state_manager.input_data.resources.werkingsgebied_repository.all()
        )
        # werkingsgebieden: List[Werkingsgebied] = [w for w in all_werkingsgebieden if w.New]
        werkingsgebieden = sorted(all_werkingsgebieden, key=lambda w: w.Title)

        content = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageWerkingsgebieden.xml",
            werkingsgebieden=werkingsgebieden,
        )

        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        ewid_service = EWIDService(
            state_manager=self._state_manager,
            wid_prefix=f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}",
            known_wid_map=self._state_manager.input_data.get_known_wid_map(),
            known_wids=self._state_manager.input_data.get_known_wids(),
        )
        content = ewid_service.add_ewids(content)

        # Resolve the wid from the werkingsgebieden
        content = self._create_werkingsgebieden_wid_lookup(content)

        return content

    def _create_werkingsgebieden_wid_lookup(self, xml_content: str):
        root = etree.fromstring(xml_content)
        elements = root.xpath("//*[@data-info-werkingsgebied-uuid]")

        for element in elements:
            uuid = element.get("data-info-werkingsgebied-uuid")
            eid = element.get("eId")
            # Set the werkingsgebied eid in the StateManager
            self._state_manager.werkingsgebied_eid_lookup[uuid] = eid
            del element.attrib["data-info-werkingsgebied-uuid"]

        return etree.tostring(root, encoding="unicode", pretty_print=True)
