from copy import copy
from uuid import UUID

from bs4 import BeautifulSoup
from lxml import etree

from ........models import PublicationSettings
from ........services.ewid.ewid_service import EWIDService
from ........services.tekst.middleware import middleware_enrich_table, middleware_image_in_p
from ........services.tekst.tekst import Lichaam
from ........services.utils.helpers import is_html_valid
from .......state_manager.input_data.resource.asset.asset import Asset
from .......state_manager.input_data.resource.asset.asset_repository import AssetRepository
from .......state_manager.state_manager import StateManager


class RegelingVrijetekstTekstGenerator:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self, html: str):
        tekst: str = self._html_to_xml_lichaam(html)
        self._state_manager.debug["tekst-part-1"] = copy(tekst)

        tekst = self._enrich_illustratie(tekst)
        self._state_manager.debug["tekst-part-2"] = copy(tekst)

        tekst = self._add_ewids(tekst)
        self._state_manager.debug["tekst-part-3"] = copy(tekst)

        tekst = self._remove_hints(tekst)
        self._state_manager.debug["tekst-part-4"] = copy(tekst)

        return tekst

    def _html_to_xml_lichaam(self, html: str) -> str:
        if not is_html_valid(html):
            raise RuntimeError("Invalid html")

        html = middleware_enrich_table(html)
        html = middleware_image_in_p(html)
        self._state_manager.debug["tekst-part-0"] = copy(html)

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
        settings: PublicationSettings = self._state_manager.input_data.publication_settings

        ewid_service = EWIDService(
            state_manager=self._state_manager,
            wid_prefix=f"{settings.provincie_id}_{settings.wId_suffix}",
        )
        result: str = ewid_service.modify_xml(xml_source=xml_data)
        return result

    def _remove_hints(self, xml_data: str) -> str:
        xml_data = self._clean_attribute(xml_data, "data-hint-gebied-code")
        xml_data = self._clean_attribute(xml_data, "data-hint-object-code")
        return xml_data

    def _clean_attribute(self, xml_data: str, attribute: str) -> str:
        root = etree.fromstring(xml_data)
        for element in root.xpath(f"//*[@{attribute}]"):
            element.attrib.pop(attribute)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
