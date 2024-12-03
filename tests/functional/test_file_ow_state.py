from typing import Set
import pytest

from dso.act_builder.state_manager.state_manager import StateManager
from dso.services.ow.models import OWGebiedenGroep, OWGebied, OWTekstdeel, OWDivisieTekst, OWDivisie


# These scenarios will be testing with functional test case
TEST_SCENARIO_DIRS = [
    "./input/01-initial",
]


@pytest.mark.parametrize("input_dir", TEST_SCENARIO_DIRS, indirect=True)
@pytest.mark.usefixtures("initialize_dso_builder")
class TestOWState:
    """
    Note:
    Following tests do not require expected_results file but generically tests the OW State.
    Mostly useful to smoke test full data exports too large for
    maintaining expected results files.
    """

    state_manager: StateManager

    def test_unused_locations_terminated(self):
        used_gebied_codes = [
            w.Code for w in self.state_manager.input_data.resources.werkingsgebied_repository._werkingsgebieden.values()
        ]
        # Build set of used gebied codes in previous state
        existing_used_gebiedengroepen = {
            self.state_manager.input_data.ow_data.ow_objects[v.locaties[0]].mapped_geo_code
            for v in self.state_manager.input_data.ow_data.ow_objects.values()
            if isinstance(v, OWTekstdeel)
        }

        # Remove new state used_gebied_codes to get leftover diff
        diff = existing_used_gebiedengroepen - set(used_gebied_codes)

        # Expecting any leftover gebied_codes from previous state to now
        # be in termination for both gebied and gebiedengroep
        terminated_gebieden_codes = [
            obj.mapped_geo_code
            for obj in self.state_manager.ow_repository._terminated_ow_objects
            if isinstance(obj, OWGebied)
        ]
        terminated_gebiedengroepen_codes = [
            obj.mapped_geo_code
            for obj in self.state_manager.ow_repository._terminated_ow_objects
            if isinstance(obj, OWGebiedenGroep)
        ]

        for gebied_code in diff:
            assert gebied_code in terminated_gebieden_codes
            assert gebied_code in terminated_gebiedengroepen_codes

        assert len(terminated_gebieden_codes) == len(diff)
        assert len(terminated_gebiedengroepen_codes) == len(diff)

    def test_new_locations(self):
        """
        Compares
            - input data used gebied codes
            - existing used gebied codes
        and tests if any new codes from this diff are added to the OW State.
        """
        used_gebied_codes = [
            w.Code for w in self.state_manager.input_data.resources.werkingsgebied_repository._werkingsgebieden.values()
        ]
        # Build set of used gebied codes in previous state
        existing_used_gebiedengroepen: Set[OWGebiedenGroep] = {
            self.state_manager.input_data.ow_data.ow_objects[v.locaties[0]].mapped_geo_code
            for v in self.state_manager.input_data.ow_data.ow_objects.values()
            if isinstance(v, OWTekstdeel)
        }

        new_gebied_codes = set(used_gebied_codes) - existing_used_gebiedengroepen

        # test new added for both gebied and gebiedengroep
        new_gebieden_codes = [
            obj.mapped_geo_code for obj in self.state_manager.ow_repository._new_ow_objects if isinstance(obj, OWGebied)
        ]
        new_gebiedengroepen_codes = [
            obj.mapped_geo_code
            for obj in self.state_manager.ow_repository._new_ow_objects
            if isinstance(obj, OWGebiedenGroep)
        ]

        for gebied_code in new_gebied_codes:
            assert gebied_code in new_gebieden_codes
            assert gebied_code in new_gebiedengroepen_codes

    def test_mutated_gebieden(self):
        # new gebieden data
        input_gebieden = self.state_manager.input_data.resources.werkingsgebied_repository._werkingsgebieden
        input_gebieden_code_identifiers = {}
        for location in input_gebieden.values():
            input_gebieden_code_identifiers[location.Code] = location.Identifier

        # search existing ow data for changed uuids
        # between reused state ow_objs and input gebieden
        expected_mutations = [
            (ow_obj.OW_ID, input_gebieden_code_identifiers[ow_obj.mapped_geo_code])
            for ow_obj in self.state_manager.input_data.ow_data.ow_objects.values()
            if isinstance(ow_obj, OWGebied)
            and ow_obj.mapped_geo_code in input_gebieden_code_identifiers
            and input_gebieden_code_identifiers[ow_obj.mapped_geo_code] != ow_obj.gio_ref
        ]

        # test if mutated uuids are set in the result state
        for ow_id, expected_uuid in expected_mutations:
            result_ow_obj = self.state_manager.ow_object_state.ow_objects[ow_id]
            assert result_ow_obj.gio_ref == str(expected_uuid), f"Expected UUID {expected_uuid} for OW ID {ow_id}"

    def test_divisions_terminated(self):
        input_data = self.state_manager.input_data

        # Get current policy object codes from repository
        input_objects = input_data.resources.policy_object_repository._data

        # get existing ow state used policy object codes
        orphaned_ow_ids = []
        orphaned_objs = []
        for owid, ow_obj in input_data.ow_data.ow_objects.items():
            if isinstance(ow_obj, OWDivisieTekst) and ow_obj.mapped_policy_object_code not in input_objects:
                orphaned_ow_ids.append(owid)
                orphaned_objs.append(ow_obj)

        # verify removed from result state
        assert not any(owid in self.state_manager.ow_object_state.ow_objects for owid in orphaned_ow_ids)
        assert all(owid in self.state_manager.ow_object_state.terminated_ow_ids for owid in orphaned_ow_ids)

    def test_annotation_refs_match_ow_state(self):
        """
        loop the annotation map and check if the expected OW objects are present
        """
        assert len(self.state_manager.annotation_ref_lookup_map) > 0, "No annotations were added to the state manager"
        assert self.state_manager.ow_object_state is not None, "OW object state expected to be set"

        annotation_type_count = {
            "gebied": 0,
            "ambtsgebied": 0,
            "gebiedsaanwijzing": 0,
        }

        for key, annotation_ref in self.state_manager.annotation_ref_lookup_map.items():
            match annotation_ref["type_annotation"]:
                case "gebied":
                    annotation_type_count["gebied"] += 1
                    gebied_code = annotation_ref["gebied_code"]
                    ow_gebiedengroep_found = any(
                        isinstance(obj, OWGebiedenGroep) and obj.mapped_geo_code == gebied_code
                        for obj in self.state_manager.ow_object_state.ow_objects.values()
                    )

                    ow_gebied_found = any(
                        isinstance(obj, OWGebied) and obj.mapped_geo_code == gebied_code
                        for obj in self.state_manager.ow_object_state.ow_objects.values()
                    )
                    assert (
                        ow_gebiedengroep_found
                    ), f"OWGebiedengroep with gebied_code {gebied_code} not found in ow_object_state"
                    assert ow_gebied_found, f"OWGebied with gebied_code {gebied_code} not found in ow_object_state"
                case "ambtsgebied":
                    annotation_type_count["ambtsgebied"] += 1
                    object_code = annotation_ref["object_code"]
                    ow_divisie_found = any(
                        isinstance(obj, (OWDivisieTekst, OWDivisie))
                        and obj.mapped_policy_object_code == object_code
                        and obj.wid == annotation_ref["wid"]
                        for obj in self.state_manager.ow_object_state.ow_objects.values()
                    )
                    assert ow_divisie_found, f"Expected ambtsgebied annotated OWDivisie with object_code {object_code}"
                case "gebiedsaanwijzing":
                    annotation_type_count["gebiedsaanwijzing"] += 1
                    # TOOD: add assertions for gebiedsaanwijzing
                case _:
                    raise ValueError("unexpected annotation type")
