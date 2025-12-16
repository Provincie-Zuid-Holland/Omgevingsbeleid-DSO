from typing import List

from dso.act_builder.services.ow.input.models import OwInputGebiedengroep, OwInputGio, OwInputLocatie
from dso.act_builder.state_manager.input_data.resource.gebieden.gebiedengroep_repository import GebiedengroepRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import GioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import GebiedenGroep, Gio
from dso.act_builder.state_manager.state_manager import StateManager


class OwInputGebiedengroepenFactory:
    def __init__(self, state_manager: StateManager):
        self._groep_repository: GebiedengroepRepository = state_manager.input_data.resources.gebiedengroep_repository
        self._gio_repository: GioRepository = state_manager.input_data.resources.gio_repository

    def get_gebiedengroepen(self) -> List[OwInputGebiedengroep]:
        gebiedengroepen: List[GebiedenGroep] = self._groep_repository.all()
        result: List[OwInputGebiedengroep] = []

        # We dont need to worry about duplicates as the OwState machine takes care of that
        for groep in gebiedengroepen:
            input_gios: List[OwInputGio] = []

            for gio_key in groep.gio_keys:
                gio: Gio = self._gio_repository.get_by_key(gio_key)
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
                input_gios.append(input_gio)

            input_gebiedengroep = OwInputGebiedengroep(
                source_code=groep.code,
                title=groep.title,
                gios=input_gios,
            )
            result.append(input_gebiedengroep)

        return result
