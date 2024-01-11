from typing import List

from dso.builder.state_manager.input_data.resource.policy_object.policy_object_repository import PolicyObjectRepository
from dso.services.utils.helpers import load_json_data
from dso.services.utils.os import create_normalized_path


class PolicyObjectResourceLoader:
    def __init__(self, base_dir: str, policy_object_files: List[str]):
        self._base_dir: str = base_dir
        self._policy_object_files: List[str] = policy_object_files

    def load(self) -> PolicyObjectRepository:
        repository = PolicyObjectRepository()

        for policy_object_file in self._policy_object_files:
            path = create_normalized_path(self._base_dir, policy_object_file)
            objects = load_json_data(path)
            repository.add_list(objects)

        return repository
