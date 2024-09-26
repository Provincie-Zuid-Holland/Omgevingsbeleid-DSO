from typing import Optional
from ....services.ow.enums import OwProcedureStatus
from ...state_manager.states.ow_repository import OWStateRepository


class BuilderContext:
    """Holds shared configuration and state for OW builders."""

    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        ow_procedure_status: Optional[OwProcedureStatus],
        orphaned_wids: list,
        ow_repository: OWStateRepository,
    ):
        self.provincie_id = provincie_id
        self.levering_id = levering_id
        self.ow_procedure_status = ow_procedure_status
        self.orphaned_wids = orphaned_wids
        self.ow_repository = ow_repository

