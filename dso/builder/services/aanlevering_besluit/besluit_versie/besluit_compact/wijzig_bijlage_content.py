from ......models import PublicationSettings
from ......services.utils.helpers import load_template
from .....state_manager.state_manager import StateManager
from .wijzig_bijlage.bijlage_werkingsgebieden_content import BijlageWerkingsgebiedenContent
from .wijzig_bijlage.lichaam_content import LichaamContent


class WijzigBijlageContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        # bijlage_werkingsgebieden needs to go first because it changes the state_manager
        bijlage_werkingsgebieden: str = BijlageWerkingsgebiedenContent(self._state_manager).create()
        lichaam: str = LichaamContent(self._state_manager).create()

        settings: PublicationSettings = self._state_manager.input_data.publication_settings

        content = load_template(
            "akn/besluit_versie/besluit_compact/WijzigBijlage.xml",
            regeling_frbr=settings.regeling_frbr,
            lichaam=lichaam,
            bijlage_werkingsgebieden=bijlage_werkingsgebieden,
            regeling_opschrift=self._state_manager.input_data.besluit.regeling_opschrift,
            componentnaam=settings.regeling_componentnaam,
            wid_prefix=f"{settings.provincie_id}_{settings.regeling_frbr.Expression_Version}__",
        )
        return content
