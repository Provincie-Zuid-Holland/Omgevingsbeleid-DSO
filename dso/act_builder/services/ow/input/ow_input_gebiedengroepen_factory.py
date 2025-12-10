from typing import List

from dso.act_builder.services.ow.input.models import OwInputGebiedengroep, OwInputGeoGio, OwInputLocatie
from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedengroep_repository import GebiedengroepRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.geogio_repository import GeoGioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import GebiedenGroep, GeoGio
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputGebiedengroepenFactory:
    def __init__(self, state_manager: StateManager):
        self._groep_repository: GebiedengroepRepository = state_manager.input_data.resources.gebiedengroep_repository
        self._gio_repository: GeoGioRepository = state_manager.input_data.resources.geogio_repository

    def get_gebiedengroepen(self) -> List[OwInputGebiedengroep]:
        gebiedengroepen: List[GebiedenGroep] = self._groep_repository.all()
        result: List[OwInputGebiedengroep] = []

        # We dont need to worry about duplicates as the OwState machine takes care of that
        for groep in gebiedengroepen:
            gio: GeoGio = self._gio_repository.get_by_key(groep.geo_gio_key)

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
            input_gebiedengroep = OwInputGebiedengroep(
                source_code=groep.code,
                title=groep.title,
                geogio=input_gio,
            )
            result.append(input_gebiedengroep)

        return result
