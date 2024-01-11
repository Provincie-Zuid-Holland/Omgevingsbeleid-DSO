from ....state_manager.state_manager import StateManager
from .....services.utils.helpers import load_template


class ProcedureverloopContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        content = load_template(
            "templates/akn/besluit_versie/Procedureverloop.xml",
            procedure=self._state_manager.input_data.procedure_verloop,
        )
        return content
