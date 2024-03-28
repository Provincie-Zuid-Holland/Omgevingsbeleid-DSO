from .....services.utils.helpers import load_template
from ....state_manager.state_manager import StateManager


class KennisgevingMetadataContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        content = load_template(
            "akn_kennisgeving/kennisgeving_versie/KennisgevingMetadata.xml",
            provincie_ref=self._state_manager.input_data.provincie_ref,
            kennisgeving=self._state_manager.input_data.kennisgeving,
        )
        return content
