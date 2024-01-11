from typing import Union

from bs4 import BeautifulSoup, Tag

from dso.services.tekst.middleware import middleware_enrich_table
from dso.services.tekst.tekst import Divisie


def html_to_divisie(html: str) -> Divisie:
    html = middleware_enrich_table(html)
    soup = BeautifulSoup(html, "html.parser")
    divisie: Divisie = Divisie()
    divisie.consume_children(soup.children)
    return divisie


def divisie_to_xml(divisie: Divisie) -> str:
    soup = BeautifulSoup(features="xml")
    xml: Union[Tag, str] = divisie.as_xml(soup)
    return str(xml)
