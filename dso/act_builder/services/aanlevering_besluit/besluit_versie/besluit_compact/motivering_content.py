from typing import Optional

from bs4 import BeautifulSoup

from ......models import PublicationSettings
from ......services.tekst.tekst import Divisietekst
from ......services.utils.helpers import load_template
from .....state_manager.input_data.besluit import Motivering
from .....state_manager.state_manager import StateManager


class MotiveringContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        motivering: Optional[Motivering] = self._state_manager.input_data.besluit.motivering
        if motivering is None:
            return ""

        wid_prefix: str = f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}__"
        motivering_eid: str = "acc"
        motivering_wid: str = f"{wid_prefix}{motivering_eid}"

        xml_content: str = self._html_to_xml_divisietekst(motivering.content)
        motivering_content: str = self._state_manager.act_ewid_service.add_ewids(
            xml_content,
            motivering_eid,
            motivering_wid,
            "Motivering",
        )

        content = load_template(
            "akn/besluit_versie/besluit_compact/Motivering.xml",
            motivering_eid=motivering_eid,
            motivering_wid=motivering_wid,
            opschrift=motivering.opschrift,
            inhoud=motivering_content,
        )

        return content

    def _html_to_xml_divisietekst(self, html: str) -> str:
        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Divisietekst()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml
