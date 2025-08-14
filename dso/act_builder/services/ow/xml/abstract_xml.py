import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Set

from dso.act_builder.services.ow.state.models import BaseOwObject
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData
from dso.act_builder.state_manager.models import OutputFile, StrContentData
from dso.act_builder.state_manager.state_manager import StateManager
from dso.models import ContentType
from dso.services.utils.helpers import load_template


@dataclass
class BuildFileResult:
    output_file: OutputFile
    object_types: List[str]


class AbstractXmlFile(ABC):
    def __init__(self, state_manager: StateManager):
        self._dataset: str = state_manager.input_data.ow_dataset
        self._area_title: str = state_manager.input_data.ow_gebied
        self._delivery_id: str = state_manager.input_data.publication_settings.opdracht.id_levering

    @abstractmethod
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        pass

    def _do_build(
        self,
        xml_filename: str,
        object_types: List[str],
        ow_objects: Set[BaseOwObject],
        output_filename: str,
    ) -> Optional[BuildFileResult]:
        if len(ow_objects) == 0:
            return None

        content: str = load_template(
            template_name=os.path.join("ow/", xml_filename),
            pretty_print=True,
            ow_objects=ow_objects,
            dataset=self._dataset,
            area_title=self._area_title,
            delivery_id=self._delivery_id,
            object_types=object_types,
        )
        output_file = OutputFile(
            filename=output_filename,
            content_type=ContentType.XML,
            content=StrContentData(content),
        )

        return BuildFileResult(
            output_file=output_file,
            object_types=object_types,
        )
