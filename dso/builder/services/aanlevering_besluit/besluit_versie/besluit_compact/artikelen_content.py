from typing import List, Optional

import roman
from bs4 import BeautifulSoup

from ......models import PublicationSettings
from ......services.tekst.tekst import Inhoud
from ......services.utils.helpers import load_template
from .....state_manager.input_data.besluit import Besluit
from .....state_manager.state_manager import StateManager
from .....state_manager.states.artikel_eid_repository import ArtikelEidType


class ArtikelenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        besluit: Besluit = self._state_manager.input_data.besluit

        wId_prefix: str = f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}__"
        eId_prefix: str = "art_"
        eId_counter: List[int] = [1]  # List allows us to modify it, as it goes by reference

        def create_article(label, inhoud):
            nonlocal eId_counter
            eId = f"{eId_prefix}{roman.toRoman(eId_counter[0])}"
            wId = f"{wId_prefix}{eId}"
            artikel = {
                "eId": eId,
                "wId": wId,
                "label": label,
                "nummer": roman.toRoman(eId_counter[0]),
                "inhoud": inhoud,
            }
            eId_counter[0] += 1
            return artikel

        wijzig_artikel = create_article(besluit.wijzig_artikel.label, besluit.wijzig_artikel.inhoud)

        tekst_artikelen = []
        for tekst_artikel in besluit.tekst_artikelen:
            inhoud = self._html_to_xml_inhoud(tekst_artikel.inhoud)
            tekst_artikelen.append(create_article(tekst_artikel.label, inhoud))

        tijd_artikel: Optional[dict] = None
        if besluit.tijd_artikel is not None:
            tijd_artikel = create_article(besluit.tijd_artikel.label, besluit.tijd_artikel.inhoud)

        # Store the eId's as we need them later
        self._state_manager.artikel_eid.add(wijzig_artikel["eId"], ArtikelEidType.WIJZIG)
        for tekst_artikel in tekst_artikelen:
            self._state_manager.artikel_eid.add(tekst_artikel["eId"], ArtikelEidType.TEKST)

        if tijd_artikel is not None:
            self._state_manager.artikel_eid.add(tijd_artikel["eId"], ArtikelEidType.BESLUIT_INWERKINGSTIJD)

        content = load_template(
            "akn/besluit_versie/besluit_compact/Artikelen.xml",
            wijzig_artikel=wijzig_artikel,
            tekst_artikelen=tekst_artikelen,
            tijd_artikel=tijd_artikel,
        )
        return content

    def _html_to_xml_inhoud(self, html: str) -> str:
        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Inhoud()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml
