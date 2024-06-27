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
        # TODO: split to smaller unit methods
        for object_code, values in self._annotation_lookup.items():
            known_divisie = self._ow_repository.get_existing_divisie(values["wid"])
            if known_divisie:
                known_gebied_code = self._ow_repository.get_existing_werkingsgebied_code_by_divisie(known_divisie.OW_ID)
                if not known_gebied_code:
                    continue

                if values["gebied_code"] != known_gebied_code:
                    # owtekstdeel mutation needed since gebied annotation was changed for this wid
                    known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(known_divisie.OW_ID)
                    if not known_tekstdeel:
                        raise OWObjectStateException(
                            message="Expected to find tekstdeel for existing divisie",
                            ref_ow_id=known_divisie.OW_ID,
                        )

                    # find new / mutated OW groep created earlier to update for tekstdeel with
                    ow_gebiedengroep = self._ow_repository.get_gebiedengroep_by_code(values["gebied_code"])
                    if not ow_gebiedengroep:
                        raise OWObjectStateException(
                            message=f"Expected gebiedengroep with werkingsgebied: {values['gebied_code']} in new state",
                            ref_ow_id=values["gebied_code"],
                        )

                    # update OW tekstdeel with new location
                    self._mutate_text_mapping(known_tekstdeel, ow_gebiedengroep.OW_ID)
            else:
                # Unknown wid so new division + tekstdeel annotation
                new_div = self._new_divisie(values["tag"], values["wid"])
                ow_location_id = self._ow_repository.get_active_ow_location_id(values["gebied_code"])
                self._new_text_mapping(new_div.OW_ID, ow_location_id)

        # terminate removed object wids
        for wid in self._terminated_wids:
            known_divisie = self._ow_repository.get_existing_divisie(wid)
            if not known_divisie:
                raise OWObjectStateException(f"missing existing divisie ow id for terminated wid: {wid}")
            if known_divisie:
                known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(known_divisie.OW_ID)
                if not known_tekstdeel:
                    raise OWObjectStateException(
                        message="Expected to find tekstdeel for existing divisie", ref_ow_id=known_divisie.OW_ID
                    )
                known_tekstdeel.set_status_beeindig()
                known_divisie.set_status_beeindig()
                self._ow_repository.add_terminated_ow(known_tekstdeel)
                self._ow_repository.add_terminated_ow(known_divisie)

    def _new_divisie(self, tag, wid) -> OWDivisie | OWDivisieTekst:
        if tag == "Divisietekst":
            ow_div = OWDivisieTekst(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIETEKST, self._provincie_id),
                wid=wid,
                procedure_status=self._ow_procedure_status,
            )
        elif tag == "Divisie":
            ow_div = OWDivisie(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIE, self._provincie_id),
                wid=wid,
                procedure_status=self._ow_procedure_status,
            )
        else:
            raise OWObjectGenerationError("Expected annotation text tag to be either Divisie or Divisietekst.")
        self._ow_repository.add_new_ow(ow_div)
        return ow_div

    def _new_text_mapping(self, ow_div_id: str, ow_location_id: str) -> OWTekstdeel:
        ow_text_mapping = OWTekstdeel(
            OW_ID=generate_ow_id(IMOWTYPES.TEKSTDEEL, self._provincie_id),
            divisie=ow_div_id,
            locaties=[ow_location_id],
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(ow_text_mapping)
        return ow_text_mapping

    def _mutate_text_mapping(self, ow_text_mapping, ow_location_id) -> None:
        ow_text_mapping.locaties = [ow_location_id]
        self._ow_repository.add_mutated_ow(ow_text_mapping)

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

    def build_template_data(self) -> OwDivisieFileData:
        new_divisies = self._ow_repository.get_new_div()
        mutated_divisies = self._ow_repository.get_mutated_div()
        terminated_divisies = self._ow_repository.get_terminated_div()

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
