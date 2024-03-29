from .....services.utils.helpers import load_template
from ....state_manager.state_manager import StateManager
from .kennisgeving.tekst_generator import TekstGenerator


class KennisgevingContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager
        self._tekst_generator: TekstGenerator = TekstGenerator(state_manager)

    def create(self) -> str:
        html: str = self._state_manager.input_data.kennisgeving_tekst
        tekst: str = self._tekst_generator.create(html)

        content = load_template(
            "akn_kennisgeving/kennisgeving_versie/Kennisgeving.xml",
            officiele_titel=self._state_manager.input_data.kennisgeving.officiele_titel,
            tekst=tekst.encode("utf-8"),
        )
        return content
