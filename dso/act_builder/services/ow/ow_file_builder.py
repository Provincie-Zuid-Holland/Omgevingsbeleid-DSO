from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

from dso.services.ow.ow_annotation_service import AnnotationType

from ....models import ContentType
from ....services.utils.helpers import load_template
from ...state_manager.models import OutputFile, StrContentData


class OwFileBuilder(ABC):
    FILE_NAME = "owFileName.xml"
    TEMPLATE_PATH = "ow/template.xml"
    OW_ANNOTATION_TYPES: List[Type[AnnotationType]] = []

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

    def _filter_annotation_types(self, annotation_lookup_map: Dict[str, List[AnnotationType]]):
        filtered_annotation_map = {
            key: [
                annotation 
                for annotation in annotations
                if any(isinstance(annotation, t) for t in self.OW_ANNOTATION_TYPES)
            ]
            for key, annotations in annotation_lookup_map.items()
        }
        return filtered_annotation_map

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
