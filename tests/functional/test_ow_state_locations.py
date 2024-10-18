from typing import Set
import pytest

from dso.services.ow.models import OWGebiedenGroep, OWGebied, OWTekstdeel

from .base import BaseTestBuilder


@pytest.fixture(scope="class")
def input_dir(request):
    return request.param


@pytest.mark.parametrize(
    "input_dir",
    [
        "tests/fixtures/test-herziening-2024-ambtsgebied",
    ],
    indirect=True,
)
class TestOWLocations(BaseTestBuilder):

    def test_unused_locations_terminated(self):
        """
        Test if policy objects / locations that are terminated or orphaned
        are correctly marked as terminated in the OW State.
        """
        self.used_gebied_codes = [
            w.Code for w in self.state_manager.input_data.resources.werkingsgebied_repository._werkingsgebieden.values()
        ]
        # Build set of used gebied codes in previous state
        existing_used_gebiedengroepen = {
            self.state_manager.input_data.ow_data.ow_objects[v.locaties[0]].mapped_geo_code
            for v in self.state_manager.input_data.ow_data.ow_objects.values()
            if isinstance(v, OWTekstdeel)
        }

        # Remove new state used_gebied_codes to get leftover diff
        diff = existing_used_gebiedengroepen - set(self.used_gebied_codes)

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
        print(terminated_gebieden_codes)

    def test_new_locations(self):
        """
        Compares
            - input data used gebied codes
            - existing used gebied codes
        and tests if any new codes from this diff are added to the OW State.
        """
        self.used_gebied_codes = [
            w.Code for w in self.state_manager.input_data.resources.werkingsgebied_repository._werkingsgebieden.values()
        ]
        # Build set of used gebied codes in previous state
        existing_used_gebiedengroepen: Set[OWGebiedenGroep] = {
            self.state_manager.input_data.ow_data.ow_objects[v.locaties[0]].mapped_geo_code
            for v in self.state_manager.input_data.ow_data.ow_objects.values()
            if isinstance(v, OWTekstdeel)
        }

        new_gebied_codes = set(self.used_gebied_codes) - existing_used_gebiedengroepen

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
        """
        Test if locations that are mutated are correctly updated in the OW State.
        """
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

        print(len(expected_mutations), "gebied mutations found")
