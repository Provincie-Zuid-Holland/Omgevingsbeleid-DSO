from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel

from dso.act_builder.state_manager.models import OutputFile
from dso.services.ow.models import OWObject
from dso.services.ow.enums import OwProcedureStatus


class OwTemplateData(BaseModel):
    filename: str
    levering_id: str
    procedure_status: Optional[OwProcedureStatus]
    object_types: List[str]
    new_ow_objects: List[OWObject] = []
    mutated_ow_objects: List[OWObject] = []
    terminated_ow_objects: List[OWObject] = []


# add base class instead of only ABC?
class OwFileBuilder(ABC):
    FILE_NAME = "owFileName.xml"
    TEMPLATE_PATH = "ow/template.xml"

    def __init__(self):
        self.file_name = self.FILE_NAME
        self.template_path = self.TEMPLATE_PATH

    @abstractmethod
    def handle_ow_object_changes(self) -> None:
        pass

    @abstractmethod
    def create_file(self, file_data: OwTemplateData) -> OutputFile:
        pass
