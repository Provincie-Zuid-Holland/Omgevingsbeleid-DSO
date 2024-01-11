from ....services.utils.helpers import load_template
from ...state_manager.state_manager import StateManager


class RegelingVersieInformatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        content = load_template(
            "templates/akn/RegelingVersieInformatie.xml",
            regeling_frbr=self._state_manager.input_data.publication_settings.regeling_frbr,
            regeling=self._state_manager.input_data.regeling,
            provincie_ref=self._state_manager.input_data.publication_settings.provincie_ref,
            soort_bestuursorgaan=self._state_manager.input_data.publication_settings.soort_bestuursorgaan,
        )
        return content
