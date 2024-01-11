from ....services.utils.helpers import load_template
from ...state_manager.state_manager import StateManager
from .besluit_versie.besluit_compact_content import BesluitCompactContent
from .besluit_versie.besluit_metadata_content import BesluitMetadataContent
from .besluit_versie.consolidatie_informatie_content import ConsolidatieInformatieContent
from .besluit_versie.expression_identificatie_content import ExpressionIdentificatieContent
from .besluit_versie.procedureverloop_content import ProcedureverloopContent


class BesluitVersieContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        # BesluitCompact should run first as it updates the state manager
        # which other services depend on
        besluit_compact = BesluitCompactContent(self._state_manager).create()
        expression_identificatie = ExpressionIdentificatieContent(self._state_manager).create()
        besluit_metadata = BesluitMetadataContent(self._state_manager).create()
        procedureverloop = ProcedureverloopContent(self._state_manager).create()
        consolidatie_informatie = ConsolidatieInformatieContent(self._state_manager).create()

        content = load_template(
            "templates/akn/BesluitVersie.xml",
            expression_identificatie=expression_identificatie,
            besluit_metadata=besluit_metadata,
            procedureverloop=procedureverloop,
            consolidatie_informatie=consolidatie_informatie,
            besluit_compact=besluit_compact,
        )
        return content
