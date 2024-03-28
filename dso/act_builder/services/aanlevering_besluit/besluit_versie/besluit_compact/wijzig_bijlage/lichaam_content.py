from ......state_manager.state_manager import StateManager
from .lichaam.regeling_vrijetekst_html_generator import RegelingVrijetekstHtmlGenerator
from .lichaam.regeling_vrijetekst_tekst_generator import RegelingVrijetekstTekstGenerator


class LichaamContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        html: str = RegelingVrijetekstHtmlGenerator(self._state_manager).create()
        tekst: str = RegelingVrijetekstTekstGenerator(self._state_manager).create(html)

        self._state_manager.debug["html"] = html
        self._state_manager.debug["tekst"] = tekst

        return tekst
