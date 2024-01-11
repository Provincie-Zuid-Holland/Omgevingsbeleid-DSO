from dso.builder.services.aanlevering_besluit.besluit_versie.besluit_compact.wijzig_bijlage.lichaam.regeling_vrijetekst_html_generator import (
    RegelingVrijetekstHtmlGenerator,
)
from dso.builder.services.aanlevering_besluit.besluit_versie.besluit_compact.wijzig_bijlage.lichaam.regeling_vrijetekst_tekst_generator import (
    RegelingVrijetekstTekstGenerator,
)
from dso.builder.state_manager.state_manager import StateManager


class LichaamContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        html: str = RegelingVrijetekstHtmlGenerator(self._state_manager).create()
        tekst: str = RegelingVrijetekstTekstGenerator(self._state_manager).create(html)

        return tekst
