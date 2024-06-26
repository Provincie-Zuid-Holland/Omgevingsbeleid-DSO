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
        instelling_doel: str = settings.instelling_doel.frbr.get_work()

        beoogde_regeling = {
            "instrument_versie": settings.regeling_frbr.get_expression(),
            "eid": self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.WIJZIG).eid,
        }

        beoogd_informatieobjecten = []
        werkingsgebieden: List[Werkingsgebied] = (
            self._state_manager.input_data.resources.werkingsgebied_repository.all()
        )
        for werkingsgebied in werkingsgebieden:
            if werkingsgebied.New:
                eid: str = self._state_manager.werkingsgebied_eid_lookup[str(werkingsgebied.UUID)]
                beoogd_informatieobjecten.append(
                    {
                        "instrument_versie": werkingsgebied.Frbr.get_expression(),
                        "eid": f"!{settings.regeling_componentnaam}#{eid}",
                    }
                )

        tijdstempels = []
        if settings.instelling_doel.datum_juridisch_werkend_vanaf is not None:
            tijdstempels.append(
                {
                    "doel": instelling_doel,
                    "datum": settings.instelling_doel.datum_juridisch_werkend_vanaf,
                    "eid": self._state_manager.artikel_eid.find_one_by_type(ArtikelEidType.BESLUIT_INWERKINGSTIJD).eid,
                }
            )

        content = load_template(
            "akn/besluit_versie/ConsolidatieInformatie.xml",
            instelling_doel=instelling_doel,
            beoogde_regeling=beoogde_regeling,
            beoogd_informatieobjecten=beoogd_informatieobjecten,
            tijdstempels=tijdstempels,
        )
        return content
