import os
from typing import List, Optional, Set

from pydantic.main import BaseModel

from ....services.ow import (
    IMOWTYPES,
    OWAmbtsgebied,
    OWDivisie,
    OwDivisieObjectType,
    OWDivisieTekst,
    OWGebiedenGroep,
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

        self._ambtsgebied: Optional[OWAmbtsgebied] = self._ow_repository.get_active_amtsgebied()
        self._debug_enabled = os.getenv("DEBUG_MODE", "").lower() in ("true", "1")

    def handle_ow_object_changes(self):
        for division_map in self._annotation_lookup.values():
            known_divisie = self._ow_repository.get_existing_divisie(division_map["wid"])
            if known_divisie:
                self.process_existing_divisie(known_divisie, division_map)
            else:
                self.process_new_divisie(annotation_data=division_map)
        self.terminate_removed_wids()

    def process_existing_divisie(self, known_divisie: OWObject, annotation_data: dict):
        """
        Process existing divisie by comparing the current state with the new state.
        if ambtsgebied is used, the new divisie will be mapped to the active ambtsgebied.
        """
        # fetch divs existing owtekstdeel
        known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(known_divisie.OW_ID)
        if not known_tekstdeel:
            raise OWObjectStateException(
                message="No existing tekstdeel to mutate for div", ref_ow_id=known_divisie.OW_ID
            )

        match annotation_data["type_annotation"]:
            case "ambtsgebied":
                # handle annotating ambtsgebied only if changed
                if not self._ambtsgebied:
                    raise OWObjectStateException(message="Expected to find active ambtsgebied since uses_ambtsgebied")
                if known_tekstdeel.locaties[0] == self._ambtsgebied.OW_ID:
                    return  # skip mutation

                self._update_tekstdeel_location(ow_tekstdeel=known_tekstdeel, ow_location_id=self._ambtsgebied.OW_ID)
            case "gebied":
                # handle annotating a gebiedengroep only if changed
                existing_ref = self._ow_repository.get_known_state_object(known_tekstdeel.locaties[0])
                if existing_ref and isinstance(existing_ref, OWGebiedenGroep):
                    if existing_ref.mapped_geo_code == annotation_data["gebied_code"]:
                        return  # skip mutation

                # fetch latest gebied from either pending state or known state
                ow_gebiedengroep = self._ow_repository.get_active_gebiedengroep_by_code(annotation_data["gebied_code"])
                if not ow_gebiedengroep:
                    raise OWObjectStateException(
                        message=f"Mutating tekstdeel but: {annotation_data['gebied_code']} missing owlocation in state",
                    )

                self._update_tekstdeel_location(ow_tekstdeel=known_tekstdeel, ow_location_id=ow_gebiedengroep.OW_ID)
            case _:
                raise OWObjectStateException(
                    message="Requiring either gebied_code or use_ambtsgebied for annotation data in division",
                    ref_ow_id=known_divisie.OW_ID,
                )

    def process_new_divisie(self, annotation_data: dict) -> OWTekstdeel:
        """
        Generates new OW divisie(tekst) tag and a OWTekstdeel container
        with refs. Either latest known ambtsgebied with be tagged or latest location ID
        based on the area code.
        """
        new_div = self._new_divisie(
            tag=annotation_data["tag"],
            wid=annotation_data["wid"],
            object_code=annotation_data["object_code"],
        )

        match annotation_data["type_annotation"]:
            case "ambtsgebied":
                if not self._ambtsgebied:
                    raise OWObjectStateException(message="Expected to find active ambtsgebied in ow_repository")
                return self._new_text_mapping(new_div.OW_ID, [self._ambtsgebied.OW_ID])
            case "gebied":
                werkingsgebied_code = annotation_data["gebied_code"]
                active_gebiedengroep = self._ow_repository.get_gebiedengroep_by_code(werkingsgebied_code)
                if not active_gebiedengroep:
                    active_gebiedengroep = self._ow_repository.get_known_gebiedengroep_by_code(werkingsgebied_code)

                if not active_gebiedengroep:
                    raise OWObjectStateException(
                        message=f"Expected to find existing werkingsgebied: {werkingsgebied_code} in ow_repository",
                    )

                return self._new_text_mapping(new_div.OW_ID, [active_gebiedengroep.OW_ID])
            case _:
                # no direct annotations to handle now
                # assuming div to be annotated later e.g. in gebiedsaanwijzing.
                pass

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

    def _update_tekstdeel_location(self, ow_tekstdeel: OWTekstdeel, ow_location_id: str) -> None:
        new_ow_tekstdeel = ow_tekstdeel.copy(deep=True, exclude={"locaties"})
        new_ow_tekstdeel.locaties = [ow_location_id]  # supporting only 1 ref for now
        if ow_location_id == ow_tekstdeel.locaties[0]:
            raise OWObjectStateException(
                message="Mutating tekstdeel but location refs are the same",
                ref_ow_id=ow_location_id,
            )
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
