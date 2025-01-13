from dataclasses import dataclass
from typing import Set

from dso.act_builder.services.ow.state.models import BaseOwObject
from dso.act_builder.services.ow.state.ow_reference_resolver import OwReferenceResolver
from dso.act_builder.services.ow.state.ow_state import OwState
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


@dataclass
class MergeResult:
    changeset: OwXmlData
    result_state: OwState


class OwStateMerger:
    def __init__(self):
        self._reference_resolver: OwReferenceResolver = OwReferenceResolver()

    def apply_into(self, new_state: OwState, active_state: OwState):
        new_state = new_state.copy(deep=True)
        active_state = active_state.copy(deep=True)

        # We flag everyting in the active state as deleted
        # As it will be flagged to changed or unchanged when we merge the new state
        self._flag_all_new(new_state)
        self._flag_all_deleted(active_state)

        self._merge_state_field(new_state, active_state, "ambtsgebieden")
        self._merge_state_field(new_state, active_state, "regelingsgebieden")
        self._merge_state_field(new_state, active_state, "gebieden")
        self._merge_state_field(new_state, active_state, "gebiedengroepen")
        self._merge_state_field(new_state, active_state, "gebiedsaanwijzingen")
        self._merge_state_field(new_state, active_state, "divisies")
        self._merge_state_field(new_state, active_state, "divisieteksten")
        self._merge_state_field(new_state, active_state, "tekstdelen")

        active_state = self._reference_resolver.resolve_references(active_state)

        changeset_state: OwState = self._generate_changeset_state(active_state)
        result_state: OwState = self._generate_result_state(active_state)

        return MergeResult(
            changeset=OwXmlData(changeset_state),
            result_state=result_state,
        )

    def _flag_all_new(self, state: OwState) -> OwState:
        [a.flag_new() for a in state.ambtsgebieden]
        [a.flag_new() for a in state.regelingsgebieden]
        [a.flag_new() for a in state.gebieden]
        [a.flag_new() for a in state.gebiedengroepen]
        [a.flag_new() for a in state.gebiedsaanwijzingen]
        [a.flag_new() for a in state.divisies]
        [a.flag_new() for a in state.divisieteksten]
        [a.flag_new() for a in state.tekstdelen]

    def _flag_all_deleted(self, state: OwState) -> OwState:
        [a.flag_deleted() for a in state.ambtsgebieden]
        [a.flag_deleted() for a in state.regelingsgebieden]
        [a.flag_deleted() for a in state.gebieden]
        [a.flag_deleted() for a in state.gebiedengroepen]
        [a.flag_deleted() for a in state.gebiedsaanwijzingen]
        [a.flag_deleted() for a in state.divisies]
        [a.flag_deleted() for a in state.divisieteksten]
        [a.flag_deleted() for a in state.tekstdelen]

    def _merge_state_field(self, new_state: OwState, active_state: OwState, field: str):
        """
        # Its the same for this specific version working for `ambtsgebieden`
        # But instead of writing these loops for every field, we abtracted it

        for new_ambtsgebied in new_state.ambtsgebieden:
            if new_ambtsgebied not in active_state.ambtsgebieden:
                active_state.ambtsgebieden.add(new_ambtsgebied)
                continue

            for active_ambtsgebied in active_state.ambtsgebieden:
                if active_ambtsgebied == new_ambtsgebied:
                    active_ambtsgebied.merge_from(new_ambtsgebied)
        """
        for new_object in getattr(new_state, field):
            if new_object not in getattr(active_state, field):
                getattr(active_state, field).add(new_object)
                continue

            for active_object in getattr(active_state, field):
                if active_object == new_object:
                    active_object.merge_from(new_object)

    def _generate_changeset_state(self, state: OwState) -> OwState:
        # Changeset is what we use to generate the xml files
        # In those files we do not send objects that have not changed
        def filter_unchanged(ow_objects: Set[BaseOwObject]) -> Set[BaseOwObject]:
            return {x for x in ow_objects if not x.is_unchanged()}

        result: OwState = OwState(
            ambtsgebieden=filter_unchanged(state.ambtsgebieden),
            regelingsgebieden=filter_unchanged(state.regelingsgebieden),
            gebieden=filter_unchanged(state.gebieden),
            gebiedengroepen=filter_unchanged(state.gebiedengroepen),
            gebiedsaanwijzingen=filter_unchanged(state.gebiedsaanwijzingen),
            divisies=filter_unchanged(state.divisies),
            divisieteksten=filter_unchanged(state.divisieteksten),
            tekstdelen=filter_unchanged(state.tekstdelen),
        )
        return result

    def _generate_result_state(self, state: OwState) -> OwState:
        # The result state which will should store for the next iteration
        # We do not care about deleted objects by then
        def filter_deleted(ow_objects: Set[BaseOwObject]) -> Set[BaseOwObject]:
            return {x for x in ow_objects if not x.is_deleted()}

        result: OwState = OwState(
            ambtsgebieden=filter_deleted(state.ambtsgebieden),
            regelingsgebieden=filter_deleted(state.regelingsgebieden),
            gebieden=filter_deleted(state.gebieden),
            gebiedengroepen=filter_deleted(state.gebiedengroepen),
            gebiedsaanwijzingen=filter_deleted(state.gebiedsaanwijzingen),
            divisies=filter_deleted(state.divisies),
            divisieteksten=filter_deleted(state.divisieteksten),
            tekstdelen=filter_deleted(state.tekstdelen),
        )
        return result
