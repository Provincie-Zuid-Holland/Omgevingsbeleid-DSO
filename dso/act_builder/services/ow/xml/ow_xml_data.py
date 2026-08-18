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

    def get_ambtsgebieden(self) -> set[OwAmbtsgebied]:
        return self._state.ambtsgebieden

    def get_regelingsgebieden(self) -> set[OwRegelingsgebied]:
        return self._state.regelingsgebieden

    def get_gebieden(self) -> set[OwGebied]:
        return self._state.gebieden

    def get_gebiedengroepen(self) -> set[OwGebiedengroep]:
        return self._state.gebiedengroepen

    def get_gebiedsaanwijzingen(self) -> set[OwGebiedsaanwijzing]:
        return self._state.gebiedsaanwijzingen

    def get_divisies(self) -> set[OwDivisie]:
        return self._state.divisies

    def get_divisieteksten(self) -> set[OwDivisietekst]:
        return self._state.divisieteksten

    def get_tekstdelen(self) -> set[OwTekstdeel]:
        return self._state.tekstdelen
