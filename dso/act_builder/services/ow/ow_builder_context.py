from typing import List, Optional

from ....services.ow.enums import OwProcedureStatus
from ....services.ow.waardelijsten.gba_registry import GebiedsaanwijzingRegistry
from ....services.ow.waardelijsten.thema_registry import ThemaRegistry


class BuilderContext:
    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        ow_procedure_status: Optional[OwProcedureStatus],
        orphaned_wids: List[str],
        imow_value_list_version: Optional[str] = None,
    ):
        self.provincie_id = provincie_id
        self.levering_id = levering_id
        self.ow_procedure_status: Optional[OwProcedureStatus] = ow_procedure_status
        self.orphaned_wids = orphaned_wids
        self.thema_registry = ThemaRegistry(version=imow_value_list_version)
        self.gebiedsaanwijzing_registry = GebiedsaanwijzingRegistry(version=imow_value_list_version)
