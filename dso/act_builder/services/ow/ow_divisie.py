from typing import List, Optional, Set

from pydantic.main import BaseModel

from ....services.ow import (
    IMOWTYPES,
    OWDivisie,
    OwDivisieObjectType,
    OWDivisieTekst,
    OWObject,
    OWObjectGenerationError,
    OwProcedureStatus,
    OWTekstdeel,
    generate_ow_id,
)
from ...state_manager import OWObjectStateException, OWStateRepository
from .ow_file_builder import OwFileBuilder


class OwDivisieFileData(BaseModel):
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_types: List[OwDivisieObjectType]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []

    @property
    def object_type_list(self) -> List[str]:
        return [obj.value for obj in self.object_types]


class OwDivisieBuilder(OwFileBuilder):
    FILE_NAME = "owDivisies.xml"
    TEMPLATE_PATH = "ow/owDivisie.xml"

    def __init__(
        self,
        provincie_id: str,
        levering_id: str,
        annotation_lookup_map: dict,
        terminated_wids: List[str],
        ow_repository: OWStateRepository,
        ow_procedure_status: Optional[OwProcedureStatus],
    ) -> None:
        super().__init__()
        self._provincie_id = provincie_id
        self._levering_id = levering_id
        self._annotation_lookup = annotation_lookup_map
        self._terminated_wids = terminated_wids
        self._ow_repository = ow_repository
        self._ow_procedure_status = ow_procedure_status
        self._used_object_types: Set[OwDivisieObjectType] = set()

    def handle_ow_object_changes(self):
        for division_map in self._annotation_lookup.values():
            known_divisie = self._ow_repository.get_existing_divisie(division_map["wid"])
            if known_divisie:
                self.process_existing_divisie(known_divisie, division_map)
            else:
                self.process_new_divisie(division_map=division_map)
        self.terminate_removed_wids()

    def process_existing_divisie(self, known_divisie: OWObject, divisie_map: dict):
        known_gebied_code = self._ow_repository.get_existing_werkingsgebied_code_by_divisie(known_divisie.OW_ID)
        if not known_gebied_code:
            raise OWObjectStateException(
                message=f"Expected to find werkingsgebied code in input state for existing divisie: {divisie_map['wid']}",
                ref_ow_id=known_divisie.OW_ID,
            )

        if divisie_map["gebied_code"] != known_gebied_code:
            self.handle_gebied_code_mutation(known_divisie, divisie_map)

    def handle_gebied_code_mutation(self, known_divisie, values):
        known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(known_divisie.OW_ID)
        if not known_tekstdeel:
            raise OWObjectStateException(
                message="Expected to find tekstdeel for existing divisie",
                ref_ow_id=known_divisie.OW_ID,
            )

        ow_gebiedengroep = self._ow_repository.get_active_gebiedengroep_by_code(values["gebied_code"])
        if not ow_gebiedengroep:
            raise OWObjectStateException(
                message=f"Expected gebiedengroep with werkingsgebied: {values['gebied_code']} in new state",
            )

        new_ow_tekstdeel = known_tekstdeel.copy(deep=True, exclude={"locaties"})
        new_ow_tekstdeel.locaties = [ow_gebiedengroep.OW_ID]
        self._ow_repository.add_mutated_ow(new_ow_tekstdeel)

    def process_new_divisie(self, division_map: dict) -> OWTekstdeel:
        new_div = self._new_divisie(
            tag=division_map["tag"],
            wid=division_map["wid"],
            object_code=division_map["object_code"],
        )

        werkingsgebied_code = division_map["gebied_code"]

        active_gebiedengroep = self._ow_repository.get_gebiedengroep_by_code(werkingsgebied_code)
        if not active_gebiedengroep:
            active_gebiedengroep = self._ow_repository.get_known_gebiedengroep_by_code(werkingsgebied_code)

        if not active_gebiedengroep:
            raise OWObjectStateException(
                message=f"Expected to find existing werkingsgebied: {werkingsgebied_code} in ow_repository",
            )

        return self._new_text_mapping(new_div.OW_ID, [active_gebiedengroep.OW_ID])

    def terminate_removed_wids(self):
        for wid in self._terminated_wids:
            known_divisie = self._ow_repository.get_existing_divisie(wid)
            if not known_divisie:
                raise OWObjectStateException(f"missing existing divisie ow id for terminated wid: {wid}")
            if known_divisie:
                self.terminate_existing_divisie(known_divisie)

    def terminate_existing_divisie(self, known_divisie: OWObject):
        known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(known_divisie.OW_ID)
        if not known_tekstdeel:
            raise OWObjectStateException(
                message="Expected to find tekstdeel for existing divisie", ref_ow_id=known_divisie.OW_ID
            )
        known_tekstdeel.set_status_beeindig()
        known_divisie.set_status_beeindig()
        self._ow_repository.add_terminated_ow(known_tekstdeel)
        self._ow_repository.add_terminated_ow(known_divisie)

    def _new_divisie(self, tag: str, wid: str, object_code: Optional[str] = None) -> OWDivisie | OWDivisieTekst:
        if tag == "Divisietekst":
            ow_div = OWDivisieTekst(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIETEKST, self._provincie_id),
                wid=wid,
                procedure_status=self._ow_procedure_status,
                mapped_policy_object_code=object_code,
            )
        elif tag == "Divisie":
            ow_div = OWDivisie(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIE, self._provincie_id),
                wid=wid,
                procedure_status=self._ow_procedure_status,
                mapped_policy_object_code=object_code,
            )
        else:
            raise OWObjectGenerationError("Expected annotation text tag to be either Divisie or Divisietekst.")
        self._ow_repository.add_new_ow(ow_div)
        return ow_div

    def _new_text_mapping(self, ow_div_id: str, locatie_refs: List[str]) -> OWTekstdeel:
        ow_text_mapping = OWTekstdeel(
            OW_ID=generate_ow_id(IMOWTYPES.TEKSTDEEL, self._provincie_id),
            divisie=ow_div_id,
            locaties=locatie_refs,
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(ow_text_mapping)
        return ow_text_mapping

    def _update_tekstdeel_gebiedengroep(self, ow_tekstdeel: OWTekstdeel, ow_location_id: str) -> None:
        new_ow_tekstdeel = ow_tekstdeel.copy(deep=True, exclude={"locaties"})
        new_ow_tekstdeel.locaties = [ow_location_id]
        self._ow_repository.add_mutated_ow(new_ow_tekstdeel)

    def get_used_object_types(self) -> List[OwDivisieObjectType]:
        return list(self._used_object_types)

    def add_used_ow_object_types(self, ow_objects: List[OWObject]) -> None:
        for obj in ow_objects:
            if isinstance(obj, OWDivisie):
                self._used_object_types.add(OwDivisieObjectType.DIVISIE)
            elif isinstance(obj, OWDivisieTekst):
                self._used_object_types.add(OwDivisieObjectType.DIVISIETEKST)
            elif isinstance(obj, OWTekstdeel):
                self._used_object_types.add(OwDivisieObjectType.TEKSTDEEL)

    def build_template_data(self) -> Optional[OwDivisieFileData]:
        new_divisies = self._ow_repository.get_new_div()
        mutated_divisies = self._ow_repository.get_mutated_div()
        terminated_divisies = self._ow_repository.get_terminated_div()

        if not (new_divisies or mutated_divisies or terminated_divisies):
            return None

        # find all used object types for this file
        self.add_used_ow_object_types(new_divisies + mutated_divisies + terminated_divisies)

        template_data = OwDivisieFileData(
            levering_id=self._levering_id,
            object_types=self.get_used_object_types(),
            new_ow_objects=new_divisies,
            mutated_ow_objects=mutated_divisies,
            terminated_ow_objects=terminated_divisies,
            procedure_status=self._ow_procedure_status,
        )
        self.template_data = template_data
        return template_data
