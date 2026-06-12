from typing import Set

from dso.act_builder.services.ow.state.models import (
    OwAmbtsgebied,
    OwDivisie,
    OwDivisietekst,
    OwGebied,
    OwGebiedengroep,
    OwGebiedsaanwijzing,
    OwRegelingsgebied,
    OwTekstdeel,
)
from dso.act_builder.services.ow.state.ow_state import OwState


# Purpose of this class is to abstract the model itself away
# So we are less likely to abuse the models export in the xml output phase
class OwXmlData:
    def __init__(self, state: OwState):
        self._state: OwState = state

    def get_ambtsgebieden(self) -> Set[OwAmbtsgebied]:
        return self._state.ambtsgebieden

    def get_regelingsgebieden(self) -> Set[OwRegelingsgebied]:
        return self._state.regelingsgebieden

    def get_gebieden(self) -> Set[OwGebied]:
        return self._state.gebieden

    def get_gebiedengroepen(self) -> Set[OwGebiedengroep]:
        return self._state.gebiedengroepen

    def get_gebiedsaanwijzingen(self) -> Set[OwGebiedsaanwijzing]:
        return self._state.gebiedsaanwijzingen

    def get_divisies(self) -> Set[OwDivisie]:
        return self._state.divisies

    def get_divisieteksten(self) -> Set[OwDivisietekst]:
        return self._state.divisieteksten

    def get_tekstdelen(self) -> Set[OwTekstdeel]:
        return self._state.tekstdelen
