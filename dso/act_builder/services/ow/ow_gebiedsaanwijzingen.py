from typing import List, Optional, Set

from pydantic.main import BaseModel

from dso.act_builder.state_manager.exceptions import OWStateError

from ....services.ow.enums import IMOWTYPES, OwGebiedsaanwijzingObjectType, OwProcedureStatus
from ....services.ow.models import OWGebiedsaanwijzing, OWObject
from ....services.ow.ow_id import generate_ow_id
from ...state_manager.states.ow_repository import OWStateRepository
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
        provincie_id: str,
        levering_id: str,
        ow_repository: OWStateRepository,
        annotation_lookup_map: dict,
        ow_procedure_status: Optional[OwProcedureStatus],
    ) -> None:
        super().__init__()
        self._provincie_id: str = provincie_id
        self._levering_id: str = levering_id
        self._ow_procedure_status = ow_procedure_status
        self._ow_repository = ow_repository
        self._annotation_lookup_map = annotation_lookup_map
        self._used_object_types: Set[OwGebiedsaanwijzingTemplateData] = set()

    def handle_ow_object_changes(self) -> None:
        """
        Handle all OW object changes for gebiedsaanwijzingen in the state.

        - for each GBA tag we process
        - lookup parent div element and get tekstdeel (either new or known from prev state)
        - check if GBA tag matches any existing tekstdeel gebiedsaanwijzingen by element wid
        - if match, check if mutated or the same
        - if no match, create new gebiedsaanwijzing and add to tekstdeel
        """

        # process every GBA tag we found in STOP xml
        for wid, annotation in self._annotation_lookup_map.items():
            if annotation["type_annotation"] != "gebiedsaanwijzing":
                continue

            # lookup parent div element and get tekstdeel (either new or known from prev state)
            locatie = self._ow_repository.get_active_gebiedengroep_by_code(annotation["werkingsgebied_code"])
            if not locatie:
                raise OWStateError(f"Locatie not found for code {annotation['werkingsgebied_code']}")

            parent_divisie = self._ow_repository.get_active_div_by_wid(wid=annotation["parent_div"]["wid"])
            if not parent_divisie:
                raise OWStateError(
                    f"Creating gebiedsaanwijzing for non existing divisie wid {annotation['parent_div']['wid']}"
                )
            ow_tekstdeel = self._ow_repository.get_active_tekstdeel_by_div(divisie_ow_id=parent_divisie.OW_ID)
            if not ow_tekstdeel:
                raise OWStateError(
                    f"Creating gebiedsaanwijzing for non existing tekstdeel. divisie owid: {parent_divisie.OW_ID}"
                )

            new_gebiedsaanwijzing = True
            if ow_tekstdeel.gebiedsaanwijzingen:
                # check if GBA tag matches any existing tekstdeel gebiedsaanwijzingen
                for gba_ref in ow_tekstdeel.gebiedsaanwijzingen:
                    known_gba: Optional[OWGebiedsaanwijzing] = self._ow_repository.get_known_state_object(ow_id=gba_ref)
                    if known_gba and known_gba.locaties[0] == locatie.OW_ID:
                        # only create OWGebiedsaanwijzing once per locatie.
                        # STOP tekst could have multiple inline refs for the same GIO.
                        new_gebiedsaanwijzing = False
                        if known_gba.type_ != annotation["type"] or known_gba.groep != annotation["groep"]:
                            pass  # mutate

            if new_gebiedsaanwijzing:
                # no match, create new gebiedsaanwijzing and add to tekstdeel
                new_gba = self.new_ow_gebiedsaanwijzing(
                    element_wid=wid,
                    naam=locatie.noemer,
                    type=annotation["type"],
                    groep=annotation["groep"],
                    locatie_ref=locatie.OW_ID,
                )
                # set new or add to list
                if not ow_tekstdeel.gebiedsaanwijzingen:
                    ow_tekstdeel.gebiedsaanwijzingen = [new_gba.OW_ID]
                else:
                    ow_tekstdeel.gebiedsaanwijzingen.append(new_gba.OW_ID)

            # update changes in state
            self._ow_repository.update_state_tekstdeel(state_ow_id=ow_tekstdeel.OW_ID, updated_obj=ow_tekstdeel)

        return

    def new_ow_gebiedsaanwijzing(
        self, element_wid: str, naam: str, type: str, groep: str, locatie_ref: str
    ) -> OWGebiedsaanwijzing:
        new_ow_id = generate_ow_id(IMOWTYPES.GEBIEDSAANWIJZING, self._provincie_id)
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
            levering_id=self._levering_id,
            procedure_status=self._ow_procedure_status,
            object_types=[OwGebiedsaanwijzingObjectType.GEBIEDSAANWIJZING],
            new_ow_objects=new,
            mutated_ow_objects=mutated,
            terminated_ow_objects=terminated,
        )
        return template_data
