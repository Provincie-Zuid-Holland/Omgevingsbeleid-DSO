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
from ...state_manager import OWObjectStateException
from ...state_manager.states.ow_repository import OWStateRepository
from .ow_builder_context import BuilderContext
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
        context: BuilderContext,
        annotation_lookup_map: dict,
        ow_repository: OWStateRepository,
        debug_enabled: bool = False,
    ) -> None:
        super().__init__()
        self._context = context
        # Filter to only include relevant type_annotations for this builder
        self._annotation_lookup = {
            key: value for key, value in annotation_lookup_map.items()
            if value.get('type_annotation') in ["ambtsgebied", "gebied"]
        }
        self._used_object_types: Set[OwDivisieObjectType] = set()

        self._debug_enabled: bool = debug_enabled
        self._ow_repository = ow_repository
        self._ambtsgebied: Optional[OWAmbtsgebied] = self._ow_repository.get_active_amtsgebied()

    def handle_ow_object_changes(self):
        if self._context.orphaned_wids != []:
            self.terminate_removed_wids(self._context.orphaned_wids)

        for division_map in self._annotation_lookup.values():
            known_divisie = self._ow_repository.get_existing_divisie_by_mapped_code(division_map["object_code"])
            if known_divisie:
                self.process_existing_divisie(known_divisie, division_map)
            else:
                self.process_new_divisie(annotation_data=division_map)

    def process_existing_divisie(self, known_divisie: OWObject, annotation_data: dict):
        known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(known_divisie.OW_ID)
        if not known_tekstdeel:
            raise OWObjectStateException(
                message="No existing tekstdeel to mutate for div", ref_ow_id=known_divisie.OW_ID
            )

        match annotation_data["type_annotation"]:
            case "ambtsgebied":
                if not self._ambtsgebied:
                    raise OWObjectStateException(message="Expected to find active ambtsgebied since uses_ambtsgebied")
                if known_tekstdeel.locaties[0] == self._ambtsgebied.OW_ID:
                    return

                self._update_tekstdeel_location(ow_tekstdeel=known_tekstdeel, ow_location_id=self._ambtsgebied.OW_ID)
            case "gebied":
                existing_ref = self._ow_repository.get_known_state_object(known_tekstdeel.locaties[0])
                if existing_ref and isinstance(existing_ref, OWGebiedenGroep):
                    if existing_ref.mapped_geo_code == annotation_data["gebied_code"]:
                        return

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

    def process_new_divisie(self, annotation_data: dict) -> Optional[OWTekstdeel]:
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
                pass  # No direct annotations to handle now, assuming div to be annotated later.

    def terminate_removed_wids(self, orphaned_wids: List[str]):
        for wid in orphaned_wids:
            known_divisie = self._ow_repository.get_existing_divisie_by_wid(wid)
            if not known_divisie:
                raise OWObjectStateException(f"Missing existing divisie OW ID for orphaned wid: {wid}")
            self.terminate_existing_divisie(known_divisie)

            known_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(divisie_ow_id=known_divisie.OW_ID)
            if not known_tekstdeel:
                raise OWObjectStateException(
                    message="Expected to find tekstdeel for existing divisie", ref_ow_id=known_divisie.OW_ID
                )
            self.terminate_existing_tekstdeel(known_tekstdeel=known_tekstdeel)

    def terminate_existing_divisie(self, known_divisie: OWObject):
        known_divisie.set_status_beeindig()
        self._ow_repository.add_terminated_ow(known_divisie)

    def terminate_existing_tekstdeel(self, known_tekstdeel: OWTekstdeel):
        known_tekstdeel.set_status_beeindig()
        self._ow_repository.add_terminated_ow(known_tekstdeel)

    def _new_divisie(self, tag: str, wid: str, object_code: Optional[str] = None) -> OWDivisie | OWDivisieTekst:
        if tag == "Divisietekst":
            ow_div = OWDivisieTekst(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIETEKST, self._context.provincie_id),
                wid=wid,
                procedure_status=self._context.ow_procedure_status,
                mapped_policy_object_code=object_code,
            )
        elif tag == "Divisie":
            ow_div = OWDivisie(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIE, self._context.provincie_id),
                wid=wid,
                procedure_status=self._context.ow_procedure_status,
                mapped_policy_object_code=object_code,
            )
        else:
            raise OWObjectGenerationError("Expected annotation text tag to be either Divisie or Divisietekst.")
        self._ow_repository.add_new_ow(ow_div)
        return ow_div

    def _new_text_mapping(self, ow_div_id: str, locatie_refs: List[str]) -> OWTekstdeel:
        ow_text_mapping = OWTekstdeel(
            OW_ID=generate_ow_id(IMOWTYPES.TEKSTDEEL, self._context.provincie_id),
            divisie=ow_div_id,
            locaties=locatie_refs,
            procedure_status=self._context.ow_procedure_status,
        )
        self._ow_repository.add_new_ow(ow_text_mapping)
        return ow_text_mapping

    def _update_tekstdeel_location(self, ow_tekstdeel: OWTekstdeel, ow_location_id: str) -> None:
        new_ow_tekstdeel = ow_tekstdeel.copy(deep=True, exclude={"locaties"})
        new_ow_tekstdeel.locaties = [ow_location_id]  # Supporting only 1 reference for now.
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

        self.add_used_ow_object_types(new_divisies + mutated_divisies + terminated_divisies)

        template_data = OwDivisieFileData(
            levering_id=self._context.levering_id,
            object_types=self.get_used_object_types(),
            new_ow_objects=new_divisies,
            mutated_ow_objects=mutated_divisies,
            terminated_ow_objects=terminated_divisies,
            procedure_status=self._context.ow_procedure_status,
        )
        self.template_data = template_data
        return template_data
