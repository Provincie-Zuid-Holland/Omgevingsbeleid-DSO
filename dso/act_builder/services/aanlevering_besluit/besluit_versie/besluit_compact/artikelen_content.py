import re
from typing import Optional, List

from bs4 import BeautifulSoup
from pydantic import BaseModel

from ......models import PublicationSettings
from ......services.tekst.tekst import Inhoud
from ......services.utils.helpers import load_template
from .....state_manager.input_data.besluit import Besluit
from .....state_manager.state_manager import StateManager
from .....state_manager.states.artikel_eid_repository import ArtikelEidType


class ArtikelContent(BaseModel):
    eId: str
    wId: str
    nummer: str
    inhoud: str


class ArtikelenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._ref_appendix_pattern = r"\[REF_APPENDIX:([^\]]+)\]"

    def create(self) -> str:
        besluit: Besluit = self._state_manager.input_data.besluit

        # Wijziging Artikel
        wijzig_artikel = self._create_article(
            besluit.wijzig_artikel.nummer,
            besluit.wijzig_artikel.inhoud,
        )
        self._state_manager.artikel_eid.add(wijzig_artikel.eId, ArtikelEidType.WIJZIG)

        # Tijds Artikel
        tijd_artikel: Optional[ArtikelContent] = None
        if besluit.tijd_artikel is not None:
            tijd_artikel = self._create_article(
                besluit.tijd_artikel.nummer,
                besluit.tijd_artikel.inhoud,
            )
            self._state_manager.artikel_eid.add(tijd_artikel.eId, ArtikelEidType.BESLUIT_INWERKINGSTIJD)

        # Tekst Artikelen
        tekst_artikelen: List[ArtikelContent] = []
        for tekst_artikel in besluit.tekst_artikelen:
            inhoud = self._html_to_xml_inhoud(tekst_artikel.inhoud)
            inhoud = self._replace_ref_appendices(inhoud)
            artikel_content: ArtikelContent = self._create_article(tekst_artikel.nummer, inhoud)

            tekst_artikelen.append(artikel_content)
            self._state_manager.artikel_eid.add(artikel_content.eId, ArtikelEidType.TEKST)

        content = load_template(
            "akn/besluit_versie/besluit_compact/Artikelen.xml",
            wijzig_artikel=wijzig_artikel,
            tekst_artikelen=tekst_artikelen,
            tijd_artikel=tijd_artikel,
        )
        return content

    def _create_article(self, nummer: str, inhoud: str) -> ArtikelContent:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        wId_prefix: str = f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}__"
        eId_prefix: str = "art_"

        eId = f"{eId_prefix}{nummer}"
        wId = f"{wId_prefix}{eId}"
        artikel_content = ArtikelContent(
            eId=eId,
            wId=wId,
            nummer=nummer,
            inhoud=inhoud,
        )
        return artikel_content

    def _html_to_xml_inhoud(self, html: str) -> str:
        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Inhoud()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml

    def _replace_ref_appendices(self, content: str) -> str:
        matches = re.findall(self._ref_appendix_pattern, content)
        for ref_id in matches:
            search = f"[REF_APPENDIX:{ref_id}]"
            replacement = f"""<IntRef ref="cmp_{ref_id}">Bijlage {ref_id}</IntRef>"""
            content = content.replace(search, replacement)

        return content
