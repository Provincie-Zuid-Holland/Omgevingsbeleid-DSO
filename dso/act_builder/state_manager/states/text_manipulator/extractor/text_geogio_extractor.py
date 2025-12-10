from lxml import etree

from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.models import TekstBijlageGeoGio


class TextGeoGioExtractor:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def extract(self, xml_content: str):
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)
        elements = root.xpath("//*[@data-hint-geogio-key]")

        for element in elements:
            geogio_key: str = element.get("data-hint-geogio-key")
            eid: str = element.get("eId")
            wid: str = element.get("wId")

            self._state_manager.text_data.bijlage_geogios.append(
                TekstBijlageGeoGio(
                    geogio_key=geogio_key,
                    eid=eid,
                    wid=wid,
                    element=element.tag,
                )
            )
