from typing import List, Optional

from pydantic.main import BaseModel

from ....services.ow.enums import IMOWTYPES, OwGebiedsaanwijzingObjectType, OwProcedureStatus
from ....services.ow.models import OWGebiedsaanwijzing, OWObject
from ....services.ow.ow_id import generate_ow_id
from ...state_manager.exceptions import OWStateError
from ...state_manager.states.ow_repository import OWStateRepository
from .ow_builder_context import BuilderContext
from .ow_file_builder import OwFileBuilder


class OwGebiedsaanwijzingTemplateData(BaseModel):
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_types: List[OwGebiedsaanwijzingObjectType]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []

    @property
    def object_type_list(self) -> List[str]:
        return [obj.value for obj in self.object_types]


class OwGebiedsaanwijzingBuilder(OwFileBuilder):
    FILE_NAME = "owGebiedsaanwijzingen.xml"
    TEMPLATE_PATH = "ow/owGebiedsaanwijzingen.xml"

    def __init__(
        self,
        context: BuilderContext,
        annotation_lookup_map: dict,
        ow_repository: OWStateRepository,
    ) -> None:
        super().__init__()
        self._context = context
        # Filter to only include relevant type_annotations for this builder
        self._annotation_lookup = {
            key: [annotation for annotation in annotations if annotation["type_annotation"] == "gebiedsaanwijzing"]
            or None
            for key, annotations in annotation_lookup_map.items()
        }
        self._ow_repository = ow_repository

    def handle_ow_object_changes(self) -> None:
        """
        Handle all OW object changes for gebiedsaanwijzingen in the state.

        - for each GBA tag we process
        - lookup parent div element and get tekstdeel (either new or known from prev state)
        - check if GBA tag matches any existing tekstdeel gebiedsaanwijzingen by element wid
        - if match, check if mutated or the same
        - if no match, create new gebiedsaanwijzing and add to tekstdeel
        """

        for object_code, annotations in self._annotation_lookup.items():
            if not annotations:
                continue

            for gba in annotations:
                locatie = self._ow_repository.get_active_gebiedengroep_by_code(gba["werkingsgebied_code"])
                if not locatie:
                    raise OWStateError(f"Locatie not found for code {gba['werkingsgebied_code']}")

                parent_divisie = self._ow_repository.get_active_div_by_wid(wid=gba["parent_div"]["wid"])
                if not parent_divisie:
                    raise OWStateError(
                        f"Creating gebiedsaanwijzing for non-existing divisie wid {gba['parent_div']['wid']}"
                    )
                ow_tekstdeel = self._ow_repository.get_active_tekstdeel_by_div(divisie_ow_id=parent_divisie.OW_ID)
                if not ow_tekstdeel:
                    raise OWStateError(
                        f"Creating gebiedsaanwijzing for non-existing tekstdeel. divisie owid: {parent_divisie.OW_ID}"
                    )

                new_gebiedsaanwijzing = True
                # check if this gba already exists for this div
                if ow_tekstdeel.gebiedsaanwijzingen:
                    for gba_ref in ow_tekstdeel.gebiedsaanwijzingen:
                        known_gba: Optional[OWGebiedsaanwijzing] = self._ow_repository.get_known_state_object(
                            ow_id=gba_ref
                        )
                        if known_gba and known_gba.locaties[0] == locatie.OW_ID:
                            new_gebiedsaanwijzing = False
                            if known_gba.type_ != gba["type"] or known_gba.groep != gba["groep"]:
                                pass  # mutate

                if new_gebiedsaanwijzing:
                    new_gba = self.new_ow_gebiedsaanwijzing(
                        element_wid=gba["wid"],
                        naam=locatie.noemer,
                        type=gba["type"],
                        groep=gba["groep"],
                        locatie_ref=locatie.OW_ID,
                    )
                    if not ow_tekstdeel.gebiedsaanwijzingen:
                        ow_tekstdeel.gebiedsaanwijzingen = [new_gba.OW_ID]
                    else:
                        ow_tekstdeel.gebiedsaanwijzingen.append(new_gba.OW_ID)

                if new_gebiedsaanwijzing:
                    self._ow_repository.update_state_tekstdeel(state_ow_id=ow_tekstdeel.OW_ID, updated_obj=ow_tekstdeel)

    def new_ow_gebiedsaanwijzing(
        self, element_wid: str, naam: str, type: str, groep: str, locatie_ref: str
    ) -> OWGebiedsaanwijzing:
        new_ow_id = generate_ow_id(IMOWTYPES.GEBIEDSAANWIJZING, self._context.provincie_id)
        input_dict = {
            "OW_ID": new_ow_id,
            "naam": naam,
            "type_": type,
            "groep": groep,
            "locaties": [locatie_ref],
            "wid": element_wid,
        }
        gebiedawz = OWGebiedsaanwijzing(**input_dict)
        self._ow_repository.add_new_ow(gebiedawz)

        return gebiedawz

    def build_template_data(self):
        new = self._ow_repository.get_new_gebiedsaanwijzingen()
        mutated = self._ow_repository.get_mutated_gebiedsaanwijzingen()
        terminated = self._ow_repository.get_terminated_gebiedsaanwijzingen()

        if not (new or mutated or terminated):
            return None

        template_data = OwGebiedsaanwijzingTemplateData(
            levering_id=self._context.levering_id,
            procedure_status=self._context.ow_procedure_status,
            object_types=[OwGebiedsaanwijzingObjectType.GEBIEDSAANWIJZING],
            new_ow_objects=new,
            mutated_ow_objects=mutated,
            terminated_ow_objects=terminated,
        )
        return template_data
