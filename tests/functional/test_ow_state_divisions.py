import pytest

from dso.services.ow.models import OWDivisieTekst

from .base import BaseTestBuilder, TEST_SCENARIO_DIRS


@pytest.fixture(scope="class")
def input_dir(request):
    return request.param


@pytest.mark.parametrize("input_dir", TEST_SCENARIO_DIRS, indirect=True)
class TestOWDivision(BaseTestBuilder):
    def test_divisions_terminated(self):
        # self.debug()
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
