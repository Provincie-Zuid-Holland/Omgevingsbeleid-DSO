import pytest
from dso.services.ow.models import OWGebiedenGroep, OWGebied, OWDivisieTekst, OWDivisie

from .base import BaseTestBuilder


@pytest.fixture(scope="class")
def input_dir(request):
    return request.param


@pytest.mark.parametrize(
    "input_dir",
    [
        "tests/functional/scenarios/01-initial",
    ],
    indirect=True,
)
class TestOWAnnotationRefs(BaseTestBuilder):
    """
    Test that the annotation refs added to state manager have their corresponding OW objects
    """

    def test_annotation_refs_match_ow_state(self):
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