from typing import List, Optional, Set, Tuple

from pydantic.main import BaseModel

from ....services.ow.enums import IMOWTYPES, OwProcedureStatus, OwHoofdlijnObjectType
from ....services.ow.models import OWHoofdlijn, OWObject
from ....services.ow.ow_id import generate_ow_id
from ...state_manager.exceptions import OWStateError
from ...state_manager.states.ow_repository import OWStateRepository
from .ow_builder_context import BuilderContext
from .ow_file_builder import OwFileBuilder


class OwHoofdlijnTemplateData(BaseModel):
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_type_list: List[OwHoofdlijnObjectType]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []


class OwHoofdlijnBuilder(OwFileBuilder):
    FILE_NAME = "owHoofdlijnen.xml"
    TEMPLATE_PATH = "ow/owHoofdlijnen.xml"

    def __init__(
        self,
        context: BuilderContext,
        annotation_lookup_map: dict,
        ow_repository: OWStateRepository,
    ) -> None:
        super().__init__()
        self._context = context
        self._annotation_lookup = {
            key: [
                annotation for annotation in annotations
                if annotation["type_annotation"] == "hoofdlijn"
            ] or None
            for key, annotations in annotation_lookup_map.items()
        }
        self._ow_repository = ow_repository

    def handle_ow_object_changes(self) -> None:
        """
        Handle all OW object changes for hoofdlijnen in the state.

        - For each hoofdlijn annotation we process
        - Lookup tekstdeel by object code
        - For each hoofdlijn value pair (soort, name):
            - Check if hoofdlijn exists in state by soort/name
            - If exists, reuse the OW_ID
            - If new, create new hoofdlijn
            - Add hoofdlijn reference to tekstdeel
        """
        for object_code, annotations in self._annotation_lookup.items():
            if not annotations:
                continue

            for hoofdlijn_annotation in annotations:
                tekstdeel = self._ow_repository.get_active_tekstdeel_by_object_code(object_code)
                if not tekstdeel:
                    raise OWStateError(
                        f"Creating hoofdlijn for non-existing tekstdeel. object-code: {object_code}"
                    )

                hoofdlijn_refs = []
                for hoofdlijn_values in hoofdlijn_annotation["hoofdlijnen"]:
                    # check if this hoofdlijn already exists in state
                    existing_hoofdlijn = self._ow_repository.get_active_hoofdlijn_by_soort_naam(
                        soort=hoofdlijn_values["soort"],
                        naam=hoofdlijn_values["naam"]
                    )

                    if existing_hoofdlijn:
                        hoofdlijn_refs.append(existing_hoofdlijn.OW_ID)
                    else:
                        new_hoofdlijn = self.new_ow_hoofdlijn(
                            soort=hoofdlijn_values["soort"],
                            naam=hoofdlijn_values["naam"]
                        )
                        hoofdlijn_refs.append(new_hoofdlijn.OW_ID)

                # Update tekstdeel with new hoofdlijn refs, replacing any existing ones
                tekstdeel.hoofdlijnen = hoofdlijn_refs
                self._ow_repository.update_state_tekstdeel(
                    state_ow_id=tekstdeel.OW_ID,
                    updated_obj=tekstdeel
                )

    def new_ow_hoofdlijn(self, soort: str, naam: str) -> OWHoofdlijn:
        new_ow_id = generate_ow_id(IMOWTYPES.HOOFDLIJN, self._context.provincie_id)
        input_dict = {
            "OW_ID": new_ow_id,
            "soort": soort,
            "naam": naam,
        }
        hoofdlijn = OWHoofdlijn(**input_dict)
        self._ow_repository.add_new_ow(hoofdlijn)

        return hoofdlijn

    def build_template_data(self):
        new = self._ow_repository.get_new_hoofdlijnen()
        mutated = self._ow_repository.get_mutated_hoofdlijnen()
        terminated = self._ow_repository.get_terminated_hoofdlijnen()

        if not (new or mutated or terminated):
            return None

        template_data = OwHoofdlijnTemplateData(
            levering_id=self._context.levering_id,
            procedure_status=self._context.ow_procedure_status,
            object_type_list=[OwHoofdlijnObjectType.HOOFDLIJN],
            new_ow_objects=new,
            mutated_ow_objects=mutated,
            terminated_ow_objects=terminated,
        )
        return template_data
