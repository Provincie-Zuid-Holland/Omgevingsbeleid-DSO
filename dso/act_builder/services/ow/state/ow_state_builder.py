from typing import List, Optional
from uuid import uuid4

from dso.act_builder.services.ow.input.models import (
    OwInputAbstractLocatieRef,
    OwInputAmbtsgebied,
    OwInputAmbtsgebiedLocatieRef,
    OwInputGebiedsaanwijzing,
    OwInputPolicyObject,
    OwInputRegelingsgebied,
    OwInputWerkingsgebied,
    OwInputWerkingsgebiedLocatieRef,
)
from dso.act_builder.services.ow.state.models import (
    AbstractLocationRef,
    AbstractWidRef,
    OwAmbtsgebied,
    OwDivisie,
    OwDivisietekst,
    OwGebied,
    OwGebiedengroep,
    OwGebiedsaanwijzing,
    OwObjectStatus,
    OwRegelingsgebied,
    OwTekstdeel,
    UnresolvedAmbtsgebiedRef,
    UnresolvedDivisieRef,
    UnresolvedDivisietekstRef,
    UnresolvedGebiedengroepRef,
    UnresolvedGebiedRef,
)
from dso.act_builder.services.ow.state.ow_state import OwState
from dso.services.utils.waardelijsten import ProcedureType


class OwStateBuilder:
    def __init__(self, province_id: str, procedure_type: ProcedureType):
        self._province_id: str = province_id
        self._procedure_status: Optional[str] = "ontwerp" if procedure_type == ProcedureType.Ontwerpbesluit else None
        self._state: OwState = OwState()

    def add_ambtsgebied(self, input_ambtsgebied: OwInputAmbtsgebied):
        ambtsgebied = OwAmbtsgebied(
            object_status=OwObjectStatus.new,
            source_uuid=input_ambtsgebied.source_uuid,
            procedure_status=self._procedure_status,
            identification=self._generate_identifier("ambtsgebied"),
            administrative_borders_id=input_ambtsgebied.administrative_borders_id,
            domain=input_ambtsgebied.domain,
            valid_on=input_ambtsgebied.valid_on,
            title=input_ambtsgebied.title,
        )
        self._state.ambtsgebieden.add(ambtsgebied)

    def add_regelingsgebied(self, input_regelingsgebied: OwInputRegelingsgebied):
        regelingsgebied = OwRegelingsgebied(
            object_status=OwObjectStatus.new,
            source_uuid=input_regelingsgebied.source_uuid,
            procedure_status=self._procedure_status,
            identification=self._generate_identifier("regelingsgebied"),
            locatie_ref=UnresolvedAmbtsgebiedRef(),
        )
        self._state.regelingsgebieden.add(regelingsgebied)

    def add_werkingsgebieden(self, input_werkingsgebieden: List[OwInputWerkingsgebied]):
        for input_werkingsgebied in input_werkingsgebieden:
            self.add_werkingsgebied(input_werkingsgebied)

    def add_werkingsgebied(self, input_werkingsgebied: OwInputWerkingsgebied):
        for input_location in input_werkingsgebied.locations:
            gebied = OwGebied(
                object_status=OwObjectStatus.new,
                source_uuid=input_location.source_uuid,
                source_code=input_location.source_code,
                procedure_status=self._procedure_status,
                identification=self._generate_identifier("gebied"),
                title=input_location.title,
                geometry_ref=input_location.geometry_id,
            )
            self._state.gebieden.add(gebied)

        gebieden_groep = OwGebiedengroep(
            object_status=OwObjectStatus.new,
            source_uuid=input_werkingsgebied.source_uuid,
            source_code=input_werkingsgebied.source_code,
            procedure_status=self._procedure_status,
            identification=self._generate_identifier("gebiedengroep"),
            title=input_werkingsgebied.title,
            gebieden_refs=[
                UnresolvedGebiedRef(
                    target_code=l.source_code,
                )
                for l in input_werkingsgebied.locations
            ],
        )
        self._state.gebiedengroepen.add(gebieden_groep)

    def add_policy_objects(self, input_policy_objects: List[OwInputPolicyObject]):
        for input_policy_object in input_policy_objects:
            self.add_policy_object(input_policy_object)

    def add_policy_object(self, input_policy_object: OwInputPolicyObject):
        if self._is_policy_object_empty(input_policy_object):
            return

        text_ref: AbstractWidRef = self._handle_policy_object_element(input_policy_object)
        location_refs: List[AbstractLocationRef] = self._handle_locations(input_policy_object.location_refs)
        tekstdeel = OwTekstdeel(
            object_status=OwObjectStatus.new,
            source_uuid=input_policy_object.source_uuid,
            source_code=input_policy_object.source_code,
            procedure_status=self._procedure_status,
            identification=self._generate_identifier("tekstdeel"),
            idealization="http://standaarden.omgevingswet.overheid.nl/idealisatie/id/concept/Indicatief",
            text_ref=text_ref,
            location_refs=location_refs,
        )
        self._state.tekstdelen.add(tekstdeel)

    def _is_policy_object_empty(self, input_policy_object: OwInputPolicyObject) -> bool:
        if len(input_policy_object.location_refs) > 0:
            return False

        return True

    def _handle_policy_object_element(self, policy_object: OwInputPolicyObject) -> AbstractWidRef:
        match policy_object.element:
            case "divisie":
                self._state.divisies.add(
                    OwDivisie(
                        source_uuid=policy_object.source_uuid,
                        source_code=policy_object.source_code,
                        object_status=OwObjectStatus.new,
                        procedure_status=self._procedure_status,
                        identification=self._generate_identifier("divisie"),
                        wid=policy_object.wid,
                    )
                )
                return UnresolvedDivisieRef(
                    target_wid=policy_object.wid,
                )
            case "divisietekst":
                self._state.divisieteksten.add(
                    OwDivisietekst(
                        source_uuid=policy_object.source_uuid,
                        source_code=policy_object.source_code,
                        object_status=OwObjectStatus.new,
                        procedure_status=self._procedure_status,
                        identification=self._generate_identifier("divisietekst"),
                        wid=policy_object.wid,
                    )
                )
                return UnresolvedDivisietekstRef(
                    target_wid=policy_object.wid,
                )
            case _:
                raise RuntimeError("Invalid element type for policy object")

    def add_gebiedsaanwijzingen(self, input_gebiedsaanwijzingen: List[OwInputGebiedsaanwijzing]):
        for input_gebiedsaanwijzing in input_gebiedsaanwijzingen:
            self.add_gebiedsaanwijzing(input_gebiedsaanwijzing)

    def add_gebiedsaanwijzing(self, input_gebiedsaanwijzing: OwInputGebiedsaanwijzing):
        location_refs: List[AbstractLocationRef] = self._handle_locations(input_gebiedsaanwijzing.location_refs)
        gebiedsaanwijzing = OwGebiedsaanwijzing(
            object_status=OwObjectStatus.new,
            source_code=input_gebiedsaanwijzing.get_unique_key(),
            procedure_status=self._procedure_status,
            identification=self._generate_identifier("gebiedsaanwijzing"),
            title=input_gebiedsaanwijzing.title,
            indication_type=input_gebiedsaanwijzing.indication_type,
            indication_group=input_gebiedsaanwijzing.indication_group,
            location_refs=location_refs,
        )
        self._state.gebiedsaanwijzingen.add(gebiedsaanwijzing)

    def _handle_locations(self, location_refs: List[OwInputAbstractLocatieRef]) -> List[AbstractLocationRef]:
        result: List[AbstractLocationRef] = []
        for location_ref in location_refs:
            match location_ref:
                case OwInputAmbtsgebiedLocatieRef():
                    result.append(UnresolvedAmbtsgebiedRef())
                case OwInputWerkingsgebiedLocatieRef() as locatie_ref:
                    result.append(UnresolvedGebiedengroepRef(target_code=locatie_ref.code))
                case _:
                    raise RuntimeError("Invalid location_ref for policy object")
        return result

    def _generate_identifier(self, ow_type: str) -> str:
        identifier: str = f"nl.imow-{self._province_id}.{ow_type}.{uuid4().hex}"
        return identifier

    def get_state(self) -> OwState:
        return self._state
