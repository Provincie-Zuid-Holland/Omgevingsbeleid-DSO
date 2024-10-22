from pathlib import Path
import debugpy
import os
import pytest
import shutil

from dso.cmds import build_input_data_from_dir
from dso.act_builder.builder import Builder
from dso.act_builder.state_manager.input_data.input_data_loader import InputData


# These scenarios will be testing with functional test case
TEST_SCENARIO_DIRS = [
    "./input/01-initial",
]


class BaseTestBuilder:
    """
    Base test class that allows customizable input_dir per test class instance.
    """

    @pytest.fixture(scope="class", autouse=True)
    def initialize_builder(self, request, input_dir):
        """
        Class-scoped fixture to initialize the Builder object once per test class.
        Subclasses should provide the `input_dir` attribute.
        """
        # Ensure the subclass has an input_dir defined
        if input_dir is None:
            pytest.fail("No input scenario dir was provided")

        scenario_path = os.path.abspath(input_dir)

        if not os.path.isdir(scenario_path):
            pytest.fail(f"Test directory does not exist: {scenario_path}")

        # Setup Builder with the specified input directory
        data: InputData = build_input_data_from_dir(str(scenario_path))
        request.cls.builder = Builder(data)
        request.cls.state_manager = request.cls.builder._state_manager

        # Ensure the initial state is clean before running tests
        self.ensure_clean_state(state_manager=request.cls.state_manager)

        # Setup results for testing
        request.cls.builder.build_publication_files()

        # store output files for assertions
        relative_path = str(Path(input_dir).relative_to(Path(input_dir).parents[0]))
        output_dir = Path("./output") / relative_path
        if output_dir.exists() and output_dir.is_dir():
            shutil.rmtree(output_dir)  # remove existing
        request.cls.builder.save_files(str(output_dir))
        print(f"Output files saved to {output_dir}")
        request.cls.output_dir = output_dir

    def ensure_clean_state(self, state_manager):
        assert len(state_manager.output_files) == 0, "Initial state should have no output files"
        assert state_manager.annotation_ref_lookup_map == {}, "Initial state should have no annotations"
        assert state_manager.act_ewid_service.get_state_used_wid_map() == {}, "Initial state shouldnt have wids"
        assert state_manager.ow_object_state is None, "Initial state should have no OW object state"
