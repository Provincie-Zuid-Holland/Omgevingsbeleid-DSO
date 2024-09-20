import os
import re
from copy import copy, deepcopy
from uuid import UUID

from bs4 import BeautifulSoup
from lxml import etree

from ........services.tekst.middleware import middleware_enrich_table
from ........services.tekst.tekst import Lichaam
from ........services.utils.helpers import is_html_valid
from .......state_manager.input_data.resource.asset.asset import Asset
from .......state_manager.input_data.resource.asset.asset_repository import AssetRepository
from .......state_manager.state_manager import StateManager


class RegelingVrijetekstTekstGenerator:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._debug_enabled = os.getenv("DEBUG_MODE", "").lower() in ("true", "1")

    def create(self, html: str):
        tekst: str = self._html_to_xml_lichaam(html)
        self._set_debug("text-stage-xml", tekst)

        tekst = self._enrich_illustratie(tekst)
        self._set_debug("text-stage-img", tekst)

        tekst = self._add_ewids(tekst)
        self._set_debug("text-stage-ewids", tekst)

        tekst = self._handle_annotation_refs(tekst)
        self._set_debug("text-stage-annotation", tekst)

        tekst = self._remove_hints(tekst)
        self._set_debug("text-stage-deleted-hints", tekst)

        return tekst

    def _set_debug(self, key: str, value: str):
        if self._debug_enabled:
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

    def _handle_annotation_refs(self, xml_data: str) -> str:
        # annotation tags/refs left in the xml data, require ewids to be generated first.
        ewid_service = self._state_manager.act_ewid_service
        state_used_wid_map = deepcopy(ewid_service.get_state_used_wid_map())
        # annotation_map = {}
        root = etree.fromstring(xml_data)

        # Handle IntIoRef tags
        for element in root.xpath("//IntIoRef"):
            # find first parent element that is Divisietekst tag
            parent = element.getparent()
            while parent is not None and parent.tag != "Divisietekst":
                parent = parent.getparent()

            # retrieve the used inioref pointers WID from bijlage
            wid_ref_key_pattern = (
                f"bijlage-werkingsgebieden-divisietekst-referentie-{element.attrib['data-hint-locatie']}-ref"
            )
            for key, value in state_used_wid_map.items():
                if re.match(wid_ref_key_pattern, key):
                    # replace the element "ref" tag  with annotation_ref_wid
                    element.attrib["ref"] = value
                    break

            # update state with data for gebiedsaanwijzing
            self._state_manager.annotation_ref_lookup_map[element.attrib["wId"]] = {
                "type_annotation": "gebiedsaanwijzing",
                "ref": element.attrib["ref"],
                "werkingsgebied_code": element.attrib.pop("data-hint-locatie"),
                "groep": element.attrib.pop("data-hint-gebiedengroep"),
                "type": element.attrib.pop("data-hint-gebiedsaanwijzingtype"),
                "parent_div": {
                    "wid": parent.attrib["wId"],
                    "object-code": parent.attrib["data-hint-object-code"],
                    "gebied-code": parent.attrib["data-hint-gebied-code"],
                },
            }

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output

    def _remove_hints(self, xml_data: str) -> str:
        xml_data = self._clean_attribute(xml_data, "data-hint-gebied-code")
        xml_data = self._clean_attribute(xml_data, "data-hint-object-code")
        xml_data = self._clean_attribute(xml_data, "data-hint-wid-code")
        return xml_data

    def _clean_attribute(self, xml_data: str, attribute: str) -> str:
        root = etree.fromstring(xml_data)
        for element in root.xpath(f"//*[@{attribute}]"):
            element.attrib.pop(attribute)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
