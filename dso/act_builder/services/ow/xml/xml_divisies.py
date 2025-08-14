from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlDivisies(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="divisies.xml",
            object_types=["Divisie"],
            ow_objects=xml_data.get_divisies(),
            output_filename="ow-divisies.xml",
        )
