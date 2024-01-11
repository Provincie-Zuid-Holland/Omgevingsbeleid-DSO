from typing import List

from .....models import PublicationSettings
from .....services.utils.helpers import load_template
from ....state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from ....state_manager.state_manager import StateManager
from ....state_manager.states.artikel_eid_repository import ArtikelEidType


class ConsolidatieInformatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        settings: PublicationSettings = self._state_manager.input_data.publication_settings
        doel: str = f"/join/id/proces/{ settings.provincie_id }/{settings.doel.jaar}/{settings.doel.naam}"

        beoogde_regeling = {
            "instrument_versie": settings.regeling_frbr.expression,
            "eid": self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.WIJZIG).eid,
        }

        beoogd_informatieobjecten = []
        werkingsgebieden: List[
            Werkingsgebied
        ] = self._state_manager.input_data.resources.werkingsgebied_repository.all()
        for werkingsgebied in werkingsgebieden:
            eid: str = self._state_manager.werkingsgebied_eid_lookup[str(werkingsgebied.UUID)]
            beoogd_informatieobjecten.append(
                {
                    "instrument_versie": werkingsgebied.get_FRBR().expression,
                    "eid": f"!{settings.regeling_componentnaam}#{eid}",
                }
            )

        content = load_template(
            "templates/akn/besluit_versie/ConsolidatieInformatie.xml",
            doel=doel,
            beoogde_regeling=beoogde_regeling,
            beoogd_informatieobjecten=beoogd_informatieobjecten,
            tijdstempel={
                "datum": settings.datum_juridisch_werkend_vanaf,
                "eid": self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.TIJD).eid,
            },
        )
        return content
