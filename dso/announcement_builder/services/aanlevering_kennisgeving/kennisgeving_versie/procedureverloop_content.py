from .....services.utils.helpers import load_template
from ....state_manager.state_manager import StateManager


class ProcedureverloopContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        content = load_template(
            "akn_kennisgeving/kennisgeving_versie/ProcedureverloopMutatie.xml",
            procedure=self._state_manager.input_data.procedure_verloop,
        )
        return content
