from typing import List

from dso.act_builder.services.ow.input.models import (
    OwInputGebiedsaanwijzing,
    OwInputGeoGio,
    OwInputLocatie,
)
from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedsaanwijzing_repository import (
    GebiedsaanwijzingRepository,
)
from dso.act_builder.state_manager.input_data.resource.gebieden.geogio_repository import GeoGioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebiedsaanwijzing, GeoGio
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputGebiedsaanwijzingFactory:
    def __init__(self, state_manager: StateManager):
        self._aanwijzing_repository: GebiedsaanwijzingRepository = (
            state_manager.input_data.resources.gebiedsaanwijzingen_repository
        )
        self._gio_repository: GeoGioRepository = state_manager.input_data.resources.geogio_repository

    def get_gebiedsaanwijzingen(self) -> List[OwInputGebiedsaanwijzing]:
        aanwijzingen: List[Gebiedsaanwijzing] = self._aanwijzing_repository.all()
        result: List[OwInputGebiedsaanwijzing] = []

        # We dont need to worry about duplicates as the OwState machine takes care of that
        for aanwijzing in aanwijzingen:
            gio: GeoGio = self._gio_repository.get_by_key(aanwijzing.geo_gio_key)

            input_locaties: List[OwInputLocatie] = [
                OwInputLocatie(
                    source_code=locatie.code,
                    title=locatie.title,
                    geometry_id=locatie.basisgeo_id,
                )
                for locatie in gio.locaties
            ]
            input_gio: OwInputGeoGio = OwInputGeoGio(
                source_code=gio.key(),
                title=gio.title,
                locaties=input_locaties,
            )
            input_aanwijzing = OwInputGebiedsaanwijzing(
                source_code=aanwijzing.key(),
                title=aanwijzing.title,
                aanwijzing_type=aanwijzing.aanwijzing_type,
                aanwijzing_groep=aanwijzing.aanwijzing_groep,
                geogio=input_gio,
            )
            result.append(input_aanwijzing)

        return result
