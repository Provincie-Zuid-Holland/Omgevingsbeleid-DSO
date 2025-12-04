from typing import List
from unittest.mock import MagicMock, Mock

import pytest

from dso.act_builder.state_manager import StateManager, OutputFile
from dso.act_builder.state_manager.input_data.resource.resources import Resources
from dso.announcement_builder.state_manager.models import InputData
from dso.models import PublicationSettings


class StateManagerTestCase:
    def _get_output_files(self, state_manager: StateManager | MagicMock) -> List[OutputFile]:
        files: List[OutputFile] = []
        for call in state_manager.add_output_file.call_args_list:
            files.append(call.args[0])
        return files


@pytest.fixture
def state_manager_mock() -> StateManager | Mock:
    state_manager = MagicMock(spec=StateManager)
    state_manager.input_data = MagicMock(spec=InputData)
    state_manager.input_data.resources = MagicMock(spec=Resources)
    state_manager.input_data.publication_settings = MagicMock(spec=PublicationSettings)
    return state_manager
