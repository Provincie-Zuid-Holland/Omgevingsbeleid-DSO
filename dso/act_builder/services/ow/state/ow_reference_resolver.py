from dso.act_builder.services.ow.state.models import (
    AbstractRef,
    AmbtsgebiedRef,
    DivisieRef,
    DivisietekstRef,
    GebiedengroepRef,
    GebiedRef,
    UnresolvedAmbtsgebiedRef,
    UnresolvedDivisieRef,
    UnresolvedDivisietekstRef,
    UnresolvedGebiedengroepRef,
    UnresolvedGebiedRef,
    UnresolvedGebiedsaanwijzingRef,
    GebiedsaanwijzingRef,
)
from dso.act_builder.services.ow.state.ow_state import OwState


class OwReferenceResolver:
    def resolve_references(self, state: OwState) -> OwState:
        for regelingsgebied in state.regelingsgebieden:
            # Deleted objects should be removed as-is and therefor their references not be updated
            if regelingsgebied.is_deleted():
                continue
            regelingsgebied.locatie_ref = self._resolve_generic_reference(state, regelingsgebied.locatie_ref)

        for gebiedengroep in state.gebiedengroepen:
            if gebiedengroep.is_deleted():
                continue
            for index, ref in enumerate(gebiedengroep.gebieden_refs):
                gebiedengroep.gebieden_refs[index] = self._resolve_generic_reference(state, ref)

        for gebiedsaanwijzing in state.gebiedsaanwijzingen:
            if gebiedsaanwijzing.is_deleted():
                continue
            for index, ref in enumerate(gebiedsaanwijzing.location_refs):
                gebiedsaanwijzing.location_refs[index] = self._resolve_generic_reference(state, ref)

        for tekstdeel in state.tekstdelen:
            if tekstdeel.is_deleted():
                continue
            tekstdeel.text_ref = self._resolve_generic_reference(state, tekstdeel.text_ref)
            for index, ref in enumerate(tekstdeel.location_refs):
                tekstdeel.location_refs[index] = self._resolve_generic_reference(state, ref)
            for index, ref in enumerate(tekstdeel.gebiedsaanwijzing_refs):
                tekstdeel.gebiedsaanwijzing_refs[index] = self._resolve_generic_reference(state, ref)

        return state

    def _resolve_generic_reference(self, state: OwState, ref: AbstractRef) -> AbstractRef:
        match ref:
            case AmbtsgebiedRef():
                return self._resolve_ambtsgebied_ref(state)
            case UnresolvedAmbtsgebiedRef():
                return self._resolve_ambtsgebied_ref(state)
            case GebiedRef() as input_ref:
                return self._resolve_gebied_ref(state, input_ref)
            case UnresolvedGebiedRef() as input_ref:
                return self._resolve_gebied_ref(state, input_ref)
            case GebiedengroepRef() as input_ref:
                return self._resolve_gebiedengroep_ref(state, input_ref)
            case UnresolvedGebiedengroepRef() as input_ref:
                return self._resolve_gebiedengroep_ref(state, input_ref)
            case DivisieRef() as input_ref:
                return self._resolve_divisie_ref(state, input_ref)
            case UnresolvedDivisieRef() as input_ref:
                return self._resolve_divisie_ref(state, input_ref)
            case DivisietekstRef() as input_ref:
                return self._resolve_divisietekst_ref(state, input_ref)
            case UnresolvedDivisietekstRef() as input_ref:
                return self._resolve_divisietekst_ref(state, input_ref)
            case GebiedsaanwijzingRef() as input_ref:
                return self._resolve_gebiedsaanwijzing_ref(state, input_ref)
            case UnresolvedGebiedsaanwijzingRef() as input_ref:
                return self._resolve_gebiedsaanwijzing_ref(state, input_ref)
        raise RuntimeError("Unable to resolve generic reference")

    def _resolve_ambtsgebied_ref(self, state: OwState) -> AmbtsgebiedRef:
        for ambtsgebied in state.ambtsgebieden:
            if ambtsgebied.is_deleted():
                continue
            return AmbtsgebiedRef(ref=ambtsgebied.identification)
        raise RuntimeError("No ambtsgebied found to reference to")

    def _resolve_gebied_ref(self, state: OwState, input_ref: UnresolvedGebiedRef) -> GebiedRef:
        for gebied in state.gebieden:
            if gebied.is_deleted():
                continue
            if gebied.get_key() == input_ref.get_key():
                return GebiedRef(
                    target_code=input_ref.target_code,
                    ref=gebied.identification,
                )
        raise RuntimeError("No gebied found to reference to")

    def _resolve_gebiedengroep_ref(self, state: OwState, input_ref: UnresolvedGebiedengroepRef) -> GebiedengroepRef:
        for groep in state.gebiedengroepen:
            if groep.is_deleted():
                continue
            if groep.get_key() == input_ref.get_key():
                return GebiedengroepRef(
                    target_code=input_ref.target_code,
                    ref=groep.identification,
                )
        raise RuntimeError("No gebied found to reference to")

    def _resolve_divisie_ref(self, state: OwState, input_ref: UnresolvedDivisieRef) -> DivisieRef:
        for divisie in state.divisies:
            if divisie.is_deleted():
                continue
            if divisie.get_key() == input_ref.get_key():
                return DivisieRef(
                    target_wid=input_ref.target_wid,
                    ref=divisie.identification,
                )
        raise RuntimeError("No divisie found to reference to")

    def _resolve_divisietekst_ref(self, state: OwState, input_ref: UnresolvedDivisietekstRef) -> DivisietekstRef:
        for divisietekst in state.divisieteksten:
            if divisietekst.is_deleted():
                continue
            if divisietekst.get_key() == input_ref.get_key():
                return DivisietekstRef(
                    target_wid=input_ref.target_wid,
                    ref=divisietekst.identification,
                )
        raise RuntimeError("No divisietekst found to reference to")

    def _resolve_gebiedsaanwijzing_ref(self, state: OwState, input_ref: UnresolvedGebiedsaanwijzingRef) -> GebiedRef:
        for gebiedsaanwijzing in state.gebiedsaanwijzingen:
            if gebiedsaanwijzing.is_deleted():
                continue
            if gebiedsaanwijzing.get_key() == input_ref.get_key():
                return GebiedsaanwijzingRef(
                    target_key=input_ref.target_key,
                    ref=gebiedsaanwijzing.identification,
                )
        raise RuntimeError("No gebiedsaanwijzing found to reference to")
