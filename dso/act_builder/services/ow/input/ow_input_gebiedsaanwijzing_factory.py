from typing import List, Optional

from dso.act_builder.services.ow.input.models import (
    OwInputGebiedsaanwijzing,
    OwInputGio,
    OwInputLocatie,
)
from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedsaanwijzing_repository import (
    GebiedsaanwijzingRepository,
)
from dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import GioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebiedsaanwijzing, Gio
from dso.act_builder.state_manager.state_manager import StateManager
from dso.models import DocumentType
from dso.services.ow.gebiedsaanwijzingen.gebiedsaanwijzing import Gebiedsaanwijzingen, GebiedsaanwijzingenFactory
import dso.services.ow.gebiedsaanwijzingen.types as ad


class OwInputGebiedsaanwijzingFactory:
    def __init__(self, state_manager: StateManager):
        document_type: DocumentType = state_manager.input_data.publication_settings.document_type

        self._area_types: Gebiedsaanwijzingen = GebiedsaanwijzingenFactory().get_for_document(document_type)
        self._aanwijzing_repository: GebiedsaanwijzingRepository = (
            state_manager.input_data.resources.gebiedsaanwijzingen_repository
        )
        self._gio_repository: GioRepository = state_manager.input_data.resources.gio_repository

    def get_gebiedsaanwijzingen(self) -> List[OwInputGebiedsaanwijzing]:
        aanwijzingen: List[Gebiedsaanwijzing] = self._aanwijzing_repository.all()
        result: List[OwInputGebiedsaanwijzing] = []

        # We dont need to worry about duplicates as the OwState machine takes care of that
        for aanwijzing in aanwijzingen:
            gio: Gio = self._gio_repository.get_by_key(aanwijzing.gio_key)

            area_type: Optional[ad.Gebiedsaanwijzing] = self._area_types.get_by_type_label(aanwijzing.aanwijzing_type)
            if area_type is None:
                raise RuntimeError(f"Invalid gebiedsaanwijzing type `{aanwijzing.aanwijzing_type}`")
            area_value: Optional[ad.GebiedsaanwijzingWaarde] = area_type.get_value_by_label(aanwijzing.aanwijzing_groep)
            if area_value is None:
                raise RuntimeError(
                    f"Invalid gebiedsaanwijzing group `{aanwijzing.aanwijzing_groep}` for type `{aanwijzing.aanwijzing_type}`"
                )

            input_locaties: List[OwInputLocatie] = [
                OwInputLocatie(
                    source_code=locatie.code,
                    title=locatie.title,
                    geometry_id=locatie.basisgeo_id,
                )
                for locatie in gio.locaties
            ]
            input_gio: OwInputGio = OwInputGio(
                source_code=gio.key(),
                title=gio.title,
                locaties=input_locaties,
            )
            input_aanwijzing = OwInputGebiedsaanwijzing(
                source_code=aanwijzing.key(),
                title=aanwijzing.title,
                aanwijzing_type=area_type.aanwijzing_type.uri,
                aanwijzing_groep=area_value.uri,
                gio=input_gio,
            )
            result.append(input_aanwijzing)

        return result
