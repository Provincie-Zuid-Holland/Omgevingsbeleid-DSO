from typing import List
from unittest.mock import MagicMock

from dso.act_builder.state_manager import StateManager, OutputFile


class StateManagerTestCase:
    def _get_output_files(self, state_manager: StateManager | MagicMock) -> List[OutputFile]:
        files: List[OutputFile] = []
        for call in state_manager.add_output_file.call_args_list:
            files.append(call.args[0])
        return files
