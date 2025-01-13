from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlRegelingsgebieden(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="regelingsgebieden.xml",
            object_types=["Regelingsgebied"],
            ow_objects=xml_data.get_regelingsgebieden(),
            output_filename="ow-regelingsgebieden.xml",
        )
