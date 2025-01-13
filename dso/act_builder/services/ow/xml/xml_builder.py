from dataclasses import dataclass
from typing import List

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData
from dso.act_builder.services.ow.xml.xml_ambtsgebieden import XmlAmbtsgebieden
from dso.act_builder.services.ow.xml.xml_divisies import XmlDivisies
from dso.act_builder.services.ow.xml.xml_divisieteksten import XmlDivisieteksten
from dso.act_builder.services.ow.xml.xml_gebieden import XmlGebieden
from dso.act_builder.services.ow.xml.xml_gebiedengroepen import XmlGebiedengroepen
from dso.act_builder.services.ow.xml.xml_regelingsgebieden import XmlRegelingsgebieden
from dso.act_builder.services.ow.xml.xml_tekstdelen import XmlTekstdelen
from dso.act_builder.state_manager.models import OutputFile, StrContentData
from dso.act_builder.state_manager.state_manager import StateManager
from dso.models import ContentType
from dso.services.utils.helpers import load_template


@dataclass
class OwFile:
    name: str
    object_types: List[str]


class XmlBuilder:
    def __init__(self, state_manager: StateManager):
        self._type_builders: List[AbstractXmlFile] = [
            XmlAmbtsgebieden(state_manager),
            XmlRegelingsgebieden(state_manager),
            XmlGebieden(state_manager),
            XmlGebiedengroepen(state_manager),
            XmlDivisies(state_manager),
            XmlDivisieteksten(state_manager),
            XmlTekstdelen(state_manager),
        ]
        self._state_manager: StateManager = state_manager

    def build_files(self, xml_data: OwXmlData):
        ow_files: List[OwFile] = []

        for file_builder in self._type_builders:
            build_result: BuildFileResult = file_builder.build_file(xml_data)
            if build_result is None:
                continue

            self._state_manager.add_output_file(build_result.output_file)

            ow_files.append(
                OwFile(
                    name=build_result.output_file.filename,
                    object_types=build_result.object_types,
                )
            )

        manifest_content: str = load_template(
            template_name="ow/manifest.xml",
            pretty_print=True,
            ow_files=ow_files,
            act_work=self._state_manager.input_data.publication_settings.regeling_frbr.get_work(),
            purpose_id=self._state_manager.input_data.publication_settings.instelling_doel.frbr.get_work(),
        )
        manifest_file = OutputFile(
            filename="ow-manifest.xml",
            content_type=ContentType.XML,
            content=StrContentData(manifest_content),
        )
        self._state_manager.add_output_file(manifest_file)
