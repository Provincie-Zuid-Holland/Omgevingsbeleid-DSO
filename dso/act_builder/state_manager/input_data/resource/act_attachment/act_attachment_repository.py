from typing import Dict, List, Optional

from .act_attachment import ActAttachment


class ActAttachmentRepository:
    def __init__(self):
        self._act_attachments: Dict[str, ActAttachment] = {}

    def add(self, act_attachment: dict):
        uuidx: str = act_attachment["UUID"]
        self._act_attachments[uuidx] = ActAttachment.parse_obj(act_attachment)

    def add_list(self, act_attachments: List[dict]):
        for act_attachment in act_attachments:
            self.add(act_attachment)

    def get_optional(self, uuidx: str) -> Optional[ActAttachment]:
        result: Optional[ActAttachment] = self._act_attachments.get(uuidx)
        return result

    def get(self, uuidx: str) -> ActAttachment:
        result: Optional[ActAttachment] = self.get_optional(uuidx)
        if result is None:
            raise RuntimeError(f"Can not find act attachmnent with uuid `{uuidx}`")
        return result

    def all(self) -> List[ActAttachment]:
        return list(self._act_attachments.values())

    def is_empty(self) -> bool:
        return not self._act_attachments

    def to_dict(self) -> Dict[str, str]:
        serializable_data = {str(k): v.get_filename() for k, v in self._act_attachments.items()}
        return serializable_data

    def get_for_object_code(self, owner_object_code: str) -> List[ActAttachment]:
        result: List[ActAttachment] = [
            a for _, a in self._act_attachments.items() if a.owner_object_code == owner_object_code
        ]
        return result
