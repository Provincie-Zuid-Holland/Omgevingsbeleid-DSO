from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlTekstdelen(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="tekstdelen.xml",
            object_types=["Tekstdeel"],
            ow_objects=xml_data.get_tekstdelen(),
            output_filename="ow-tekstdelen.xml",
        )
