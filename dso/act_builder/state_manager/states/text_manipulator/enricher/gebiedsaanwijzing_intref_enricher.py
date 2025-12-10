from uuid import UUID
from lxml import etree

from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedsaanwijzing_repository import GebiedsaanwijzingRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.geogio_repository import GeoGioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebiedsaanwijzing, GeoGio
from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.enricher.abstract_enricher import AbstractEnricher
from dso.act_builder.state_manager.states.text_manipulator.models import TekstBijlageGeoGio, TextData


class GebiedsaanwijzingIntrefEnricher(AbstractEnricher):
    def __init__(self, state_manager: StateManager):
        self._aanwijzing_repository: GebiedsaanwijzingRepository = state_manager.input_data.resources.gebiedsaanwijzingen_repository
        self._geogio_repository: GeoGioRepository = state_manager.input_data.resources.geogio_repository
        self._text_data: TextData = state_manager.text_data

    def enrich_xml(self, xml_content: str) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)

        for intref in root.xpath("//IntIoRef[@data-hint-gebiedsaanwijzing-uuid]"):
            aanwijzing_uuid: UUID = UUID(intref.get("data-hint-gebiedsaanwijzing-uuid"))
            aanwijzing: Gebiedsaanwijzing = self._aanwijzing_repository.get(aanwijzing_uuid)
            gio: GeoGio = self._geogio_repository.get_by_key(aanwijzing.geo_gio_key)
            text_gio: TekstBijlageGeoGio = self._text_data.get_geogio_by_key(gio.key())

            intref.set("ref", text_gio.wid)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
