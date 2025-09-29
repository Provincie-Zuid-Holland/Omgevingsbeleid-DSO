from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlDivisieteksten(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="divisieteksten.xml",
            object_types=["Divisietekst"],
            ow_objects=xml_data.get_divisieteksten(),
            output_filename="ow-divisieteksten.xml",
        )
