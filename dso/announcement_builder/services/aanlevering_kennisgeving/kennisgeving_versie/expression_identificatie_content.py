from .....models import DocFRBR
from .....services.utils.helpers import load_template
from .....services.utils.waardelijsten import WorkType
from ....state_manager.state_manager import StateManager


class ExpressionIdentificatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        doc_frbr: DocFRBR = self._state_manager.input_data.bekendmaking_frbr
        content = load_template(
            "akn_kennisgeving/kennisgeving_versie/ExpressionIdentificatie.xml",
            work=doc_frbr.get_work(),
            expression=doc_frbr.get_expression(),
            soort_work=WorkType.Kennisgeving.value,
        )
        return content
