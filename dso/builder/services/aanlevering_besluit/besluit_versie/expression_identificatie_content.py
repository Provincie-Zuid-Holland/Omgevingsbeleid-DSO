from dso.builder.state_manager.state_manager import StateManager
from dso.services.utils.helpers import load_template
from dso.services.utils.waardelijsten import WorkType


class ExpressionIdentificatieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        besluit_frbr = self._state_manager.input_data.publication_settings.besluit_frbr
        content = load_template(
            "templates/akn/besluit_versie/ExpressionIdentificatie.xml",
            work=besluit_frbr.work,
            expression=besluit_frbr.expression,
            soort_work=WorkType.Besluit.value,
        )
        return content
