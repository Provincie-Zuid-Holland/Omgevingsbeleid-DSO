from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlGebiedengroepen(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="gebiedengroepen.xml",
            object_types=["Gebiedengroep"],
            ow_objects=xml_data.get_gebiedengroepen(),
            output_filename="ow-gebiedengroepen.xml",
        )
