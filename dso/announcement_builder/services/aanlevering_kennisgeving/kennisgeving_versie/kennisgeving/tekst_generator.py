from bs4 import BeautifulSoup

from ......services.tekst.middleware import middleware_enrich_table
from ......services.tekst.tekst import Lichaam
from ......services.utils.helpers import is_html_valid
from .....state_manager.state_manager import StateManager


class TekstGenerator:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self, html: str):
        tekst: str = self._html_to_xml_lichaam(html)
        tekst = self._add_ewids(tekst)

        return tekst

    def _html_to_xml_lichaam(self, html: str) -> str:
        if not is_html_valid(html):
            raise RuntimeError("Invalid html")

        html = middleware_enrich_table(html)

        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Lichaam()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml

    def _add_ewids(self, xml_data: str) -> str:
        result: str = self._state_manager.ewid_service.add_ewids(xml_data)
        return result
