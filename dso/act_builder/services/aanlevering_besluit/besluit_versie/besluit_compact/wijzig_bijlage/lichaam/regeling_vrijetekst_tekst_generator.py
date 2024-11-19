from copy import copy
from dataclasses import dataclass
from typing import Dict
from uuid import UUID

from bs4 import BeautifulSoup
from lxml import etree

from ........services.tekst.middleware import middleware_enrich_table
from ........services.tekst.tekst import Lichaam
from ........services.utils.helpers import is_html_valid
from .......state_manager.input_data.resource.asset.asset import Asset
from .......state_manager.input_data.resource.asset.asset_repository import AssetRepository
from .......state_manager.state_manager import StateManager


@dataclass
class ObjectCodeElementData:
    object_code: str
    wid: str
    eid: str
    tag_name: str


class RegelingVrijetekstTekstGenerator:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self, html: str):
        tekst: str = self._html_to_xml_lichaam(html)
        self._set_debug("text-stage-xml", tekst)

        tekst = self._enrich_illustratie(tekst)
        self._set_debug("text-stage-img", tekst)

        tekst = self._add_ewids(tekst)
        self._set_debug("text-stage-ewids", tekst)

        tekst = self._remove_hints(tekst)
        self._set_debug("text-stage-deleted-hints", tekst)

        return tekst

    def _set_debug(self, key: str, value: str):
        if self._state_manager.debug_enabled:
            self._state_manager.debug[key] = copy(value)

    def _html_to_xml_lichaam(self, html: str) -> str:
        if not is_html_valid(html):
            raise RuntimeError("Invalid html")

        html = middleware_enrich_table(html)
        self._set_debug("text-stage-html", html)

        input_soup = BeautifulSoup(html, "html.parser")
        lichaam = Lichaam()
        lichaam.consume_children(input_soup.children)

        output_soup = BeautifulSoup(features="xml")
        output = lichaam.as_xml(output_soup)
        output_xml = str(output)
        return output_xml

    def _enrich_illustratie(self, xml_data: str) -> str:
        asset_repository: AssetRepository = self._state_manager.input_data.resources.asset_repository

        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_data.encode("utf-8"), parser)
        illustrations = root.findall(".//Illustratie")
        for illustration in illustrations:
            asset_uuid: str = illustration.get("data-info-asset-uuid")
            if not asset_uuid:
                continue
            asset: Asset = asset_repository.get(UUID(asset_uuid))
            illustration.set("breedte", str(asset.Meta.Breedte))
            illustration.set("dpi", str(asset.Meta.Dpi))
            illustration.set("formaat", asset.Meta.Formaat)
            illustration.set("hoogte", str(asset.Meta.Hoogte))
            illustration.set("naam", asset.get_filename())
            illustration.set("uitlijning", asset.Meta.Uitlijning)
            del illustration.attrib["data-info-asset-uuid"]

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output

    def _add_ewids(self, xml_data: str) -> str:
        result: str = self._state_manager.act_ewid_service.add_ewids(xml_data)
        return result

    def _remove_hints(self, xml_data: str) -> str:
        attributes = [
            "data-hint-object-code",
            "data-hint-target-object-code",
            "data-hint-wid-code",
        ]

        root = etree.fromstring(xml_data)

        for attribute in attributes:
            for element in root.xpath(f"//*[@{attribute}]"):
                element.attrib.pop(attribute)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
