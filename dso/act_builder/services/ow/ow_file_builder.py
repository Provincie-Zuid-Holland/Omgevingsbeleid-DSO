from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

from ...state_manager.models import OutputFile, StrContentData
from ....services.utils.helpers import load_template
from ....models import ContentType
from ....services.ow.models import OWObject
from ....services.ow.enums import OwProcedureStatus


class OwFileBuilder(ABC):
    FILE_NAME = "owFileName.xml"
    TEMPLATE_PATH = "ow/template.xml"

    def __init__(self):
        self.file_name = self.FILE_NAME
        self.template_path = self.TEMPLATE_PATH
        self.template_data = None

    @abstractmethod
    def handle_ow_object_changes(self) -> None:
        pass

    @abstractmethod
    def build_template_data(self) -> Any:
        pass

    def create_file(self, template_data: Dict[str, Any]) -> OutputFile:
        content = load_template(
            template_name=self.template_path,
            pretty_print=True,
            data=template_data,
        )
        output_file = OutputFile(
            filename=self.file_name,
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
