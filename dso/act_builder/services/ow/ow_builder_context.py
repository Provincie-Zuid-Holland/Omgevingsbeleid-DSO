from typing import Optional, List
from ....services.ow.enums import OwProcedureStatus


class BuilderContext:
    """Holds shared configuration and state for OW builders."""

    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        ow_procedure_status: Optional[OwProcedureStatus],
        orphaned_wids: List[str],
    ):
        self.provincie_id = provincie_id
        self.levering_id = levering_id
        self.ow_procedure_status: Optional[OwProcedureStatus] = ow_procedure_status
        self.orphaned_wids = orphaned_wids

