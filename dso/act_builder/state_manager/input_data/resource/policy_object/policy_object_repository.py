from typing import Dict, List, Optional

from .policy_object import PolicyObject


class PolicyObjectRepository:
    def __init__(self):
        self._data: Dict[str, PolicyObject] = {}

    def add(self, object_code: str, policy_object: dict):
        self._data[object_code] = PolicyObject(policy_object)

    def add_list(self, policy_objects: List[dict]):
        for policy_object in policy_objects:
            self.add(
                f"{policy_object['Object_Type']}-{policy_object['Object_ID']}",
                policy_object,
            )

    def add_from_dict(self, policy_objects: Dict[str, dict]) -> None:
        for object_code, policy_object in policy_objects.items():
            self.add(object_code, policy_object)

    def get_optional(self, object_type: str, object_id: int) -> Optional[PolicyObject]:
        code: str = f"{object_type}-{object_id}"
        result: Optional[PolicyObject] = self._data.get(code, None)
        return result

    def get(self, object_type: str, object_id: int) -> PolicyObject:
        o: Optional[PolicyObject] = self.get_optional(object_type, object_id)
        if o is None:
            raise RuntimeError(f"Can not find object {object_type}-{object_id}")
        return o

    def get_by_code(self, object_code: str) -> PolicyObject:
        o: Optional[PolicyObject] = self._data.get(object_code, None)
        if o is None:
            raise RuntimeError(f"Can not find object {object_code}")
        return o

    def to_dict(self):
        return {k: v.to_dict() for k, v in self._data.items()}
