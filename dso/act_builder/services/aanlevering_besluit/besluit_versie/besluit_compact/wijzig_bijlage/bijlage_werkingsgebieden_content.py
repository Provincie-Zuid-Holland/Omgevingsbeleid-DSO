from typing import List

from lxml import etree

from .......services.utils.helpers import load_template
from ......state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ......state_manager.state_manager import StateManager


class BijlageWerkingsgebiedenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        all_werkingsgebieden: List[
            Werkingsgebied
        ] = self._state_manager.input_data.resources.werkingsgebied_repository.all()
        # werkingsgebieden: List[Werkingsgebied] = [w for w in all_werkingsgebieden if w.New]
        werkingsgebieden = sorted(all_werkingsgebieden, key=lambda w: w.Title)

        content = load_template(
            "akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageWerkingsgebieden.xml",
            werkingsgebieden=werkingsgebieden,
        )

        content = self._state_manager.act_ewid_service.add_ewids(content)
        content = self._create_werkingsgebieden_wid_lookup(content)
        content = self._remove_hints(content)

        return content

    def _create_werkingsgebieden_wid_lookup(self, xml_content: str):
        root = etree.fromstring(xml_content)
        elements = root.xpath("//*[@data-hint-werkingsgebied-uuid]")

        for element in elements:
            uuid = element.get("data-hint-werkingsgebied-uuid")
            eid = element.get("eId")
            # Set the werkingsgebied eid in the StateManager
            self._state_manager.werkingsgebied_eid_lookup[uuid] = eid

        return etree.tostring(root, encoding="unicode", pretty_print=True)

    def _remove_hints(self, xml_data: str) -> str:
        xml_data = self._clean_attribute(xml_data, "data-hint-wid-code")
        xml_data = self._clean_attribute(xml_data, "data-hint-werkingsgebied-uuid")
        return xml_data

    def _clean_attribute(self, xml_data: str, attribute: str) -> str:
        root = etree.fromstring(xml_data)
        for element in root.xpath(f"//*[@{attribute}]"):
            element.attrib.pop(attribute)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
