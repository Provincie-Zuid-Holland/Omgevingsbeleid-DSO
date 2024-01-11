from .....services.utils.helpers import load_template
from ....state_manager.state_manager import StateManager
from .besluit_compact.artikelen_content import ArtikelenContent
from .besluit_compact.wijzig_bijlage_content import WijzigBijlageContent


class BesluitCompactContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        artikelen_lichaam: str = ArtikelenContent(self._state_manager).create()
        wijzig_bijlage: str = WijzigBijlageContent(self._state_manager).create()

        content = load_template(
            "templates/akn/besluit_versie/BesluitCompact.xml",
            besluit=self._state_manager.input_data.besluit,
            artikelen_lichaam=artikelen_lichaam,
            wijzig_bijlage=wijzig_bijlage,
        )
        return content
