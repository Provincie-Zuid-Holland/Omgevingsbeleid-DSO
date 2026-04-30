from ....state_manager.state_manager import StateManager
from .....models import BillFRBR
from .....services.koop.waardelijsten.gen import Worktypes
from .....services.utils.helpers import load_template


class ExpressionIdentificatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        besluit_frbr: BillFRBR = self._state_manager.input_data.publication_settings.besluit_frbr
        content = load_template(
            "akn/besluit_versie/ExpressionIdentificatie.xml",
            work=besluit_frbr.get_work(),
            expression=besluit_frbr.get_expression(),
            soort_work=Worktypes.Besluit.value,
        )
        return content
