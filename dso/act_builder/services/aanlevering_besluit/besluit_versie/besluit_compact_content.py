from typing import Optional

from bs4 import BeautifulSoup

from .....services.tekst.tekst import Inhoud
from .....services.utils.helpers import load_template
from ....state_manager.input_data.besluit import Besluit
from ....state_manager.state_manager import StateManager
from .besluit_compact.artikelen_content import ArtikelenContent
from .besluit_compact.bijlagen_content import BijlagenContent
from .besluit_compact.motivering_content import MotiveringContent
from .besluit_compact.wijzig_bijlage_content import WijzigBijlageContent


class BesluitCompactContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        artikelen_lichaam: str = ArtikelenContent(self._state_manager).create()
        wijzig_bijlage: str = WijzigBijlageContent(self._state_manager).create()

        besluit: Besluit = self._state_manager.input_data.besluit
        aanhef_xml: str = self._html_to_xml_without_root(besluit.aanhef)
        sluiting_xml: str = self._html_to_xml_without_root(besluit.sluiting)

        ondertekening_xml: Optional[str] = None
        if besluit.ondertekening != "":
            ondertekening_xml = self._html_to_xml_without_root(besluit.ondertekening)

        bijlagen_xml: str = BijlagenContent(self._state_manager).create()
        motivering_xml: str = MotiveringContent(self._state_manager).create()

        content = load_template(
            "akn/besluit_versie/BesluitCompact.xml",
            besluit=besluit,
            artikelen_lichaam=artikelen_lichaam,
            wijzig_bijlage=wijzig_bijlage,
            aanhef_xml=aanhef_xml,
            sluiting_xml=sluiting_xml,
            ondertekening_xml=ondertekening_xml,
            bijlagen_xml=bijlagen_xml,
            motivering_xml=motivering_xml,
        )
        return content

    def _html_to_xml_without_root(self, html: str) -> str:
        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Inhoud()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        contents_without_root = "".join(str(child) for child in output.contents)
        return contents_without_root
