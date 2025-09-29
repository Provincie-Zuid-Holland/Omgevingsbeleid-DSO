from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlGebieden(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="gebieden.xml",
            object_types=["Gebied"],
            ow_objects=xml_data.get_gebieden(),
            output_filename="ow-gebieden.xml",
            procedure_status=self._procedure_status,
        )
