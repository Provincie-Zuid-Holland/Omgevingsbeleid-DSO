import re
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

        object_code_lookup: Dict[str, ObjectCodeElementData] = self._build_object_code_lookup(tekst)
        tekst = self._resolve_object_intrefs(tekst, object_code_lookup)
        self._set_debug("text-stage-object-intrefs", tekst)

        tekst = self._resolve_intiorefs(tekst)
        self._set_debug("text-stage-annotation", tekst)

        tekst = self._set_document_refs(tekst)
        self._set_debug("text-stage-document-refs", tekst)

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

    def _set_document_refs(self, xml_data: str) -> str:
        document_wid_lookup = self._state_manager.document_wid_lookup

        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_data.encode("utf-8"), parser)

        for document_intio in root.xpath("//IntIoRef[@data-hint-document-uuid]"):
            document_uuid = document_intio.get("data-hint-document-uuid")
            if document_uuid in document_wid_lookup:
                ref_value = document_wid_lookup[document_uuid]
                document_intio.set("ref", ref_value)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output

    def _build_object_code_lookup(self, xml_data: str) -> Dict[str, ObjectCodeElementData]:
        result: Dict[str, ObjectCodeElementData] = {}

        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_data.encode("utf-8"), parser)
        for object_element in root.xpath("//*[@data-hint-object-code]"):
            object_code: str = object_element.get("data-hint-object-code")
            eId: str = object_element.get("eId", "")
            wId: str = object_element.get("wId", "")
            tag_name: str = object_element.tag

            result[object_code] = ObjectCodeElementData(
                object_code=object_code,
                wid=wId,
                eid=eId,
                tag_name=tag_name,
            )

        return result

    def _resolve_object_intrefs(self, xml_data: str, object_code_lookup: Dict[str, ObjectCodeElementData]) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_data.encode("utf-8"), parser)

        for document_intref in root.xpath("//IntRef[@data-hint-target-object-code]"):
            object_code: str = document_intref.get("data-hint-target-object-code")
            if object_code not in object_code_lookup:
                raise RuntimeError(f"Trying to create internal link to unknown Object Code `{object_code}`")

            data = object_code_lookup[object_code]
            document_intref.set("ref", data.eid)
            document_intref.set("scope", data.tag_name)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output

    def _resolve_intiorefs(self, xml_data: str) -> str:
        # updates IntIoRef.ref for gebiedsaanwijzingen after EWIDs are set.
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_data.encode("utf-8"), parser)

        data_hinted_elements = root.xpath("//*[@data-hint-locatie]")
        for element in data_hinted_elements:
            gba_locatie = element.get("data-hint-locatie", None)
            wid_ref_key_pattern = f"bijlage-werkingsgebieden-divisietekst-referentie-{gba_locatie}-ref"
            for key, value in self._state_manager.act_ewid_service.get_state_used_wid_map().items():
                if re.match(wid_ref_key_pattern, key):
                    element.attrib["ref"] = value
                    break

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output

    def _remove_hints(self, xml_data: str) -> str:
        attributes = [
            "data-hint-object-code",
            "data-hint-target-object-code",
            "data-hint-wid-code",
            "data-hint-locatie",
            "data-hint-document-uuid",
        ]

        root = etree.fromstring(xml_data)

        for attribute in attributes:
            for element in root.xpath(f"//*[@{attribute}]"):
                element.attrib.pop(attribute)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
