from uuid import UUID
from lxml import etree

from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedsaanwijzing_repository import (
    GebiedsaanwijzingRepository,
)
from dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import GioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebiedsaanwijzing, Gio
from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.enricher.abstract_enricher import AbstractEnricher
from dso.act_builder.state_manager.states.text_manipulator.models import TekstBijlageGio, TextData


class GebiedsaanwijzingIntrefEnricher(AbstractEnricher):
    def __init__(self, state_manager: StateManager):
        self._aanwijzing_repository: GebiedsaanwijzingRepository = (
            state_manager.input_data.resources.gebiedsaanwijzingen_repository
        )
        self._gio_repository: GioRepository = state_manager.input_data.resources.gio_repository
        self._text_data: TextData = state_manager.text_data

    def enrich_xml(self, xml_content: str) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)

        for intref in root.xpath("//IntIoRef[@data-hint-gebiedsaanwijzing-uuid]"):
            aanwijzing_uuid: UUID = UUID(intref.get("data-hint-gebiedsaanwijzing-uuid"))
            aanwijzing: Gebiedsaanwijzing = self._aanwijzing_repository.get(aanwijzing_uuid)
            gio: Gio = self._gio_repository.get_by_key(aanwijzing.geo_gio_key)
            text_gio: TekstBijlageGio = self._text_data.get_gio_by_key(gio.key())

            intref.set("ref", text_gio.wid)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
