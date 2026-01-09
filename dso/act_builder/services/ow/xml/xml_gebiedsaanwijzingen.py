from typing import Optional

from dso.act_builder.services.ow.xml.abstract_xml import AbstractXmlFile, BuildFileResult
from dso.act_builder.services.ow.xml.ow_xml_data import OwXmlData


class XmlGebiedsaanwijzingen(AbstractXmlFile):
    def build_file(self, xml_data: OwXmlData) -> Optional[BuildFileResult]:
        return self._do_build(
            xml_filename="gebiedsaanwijzingen.xml",
            object_types=["Gebiedsaanwijzing"],
            ow_objects=xml_data.get_gebiedsaanwijzingen(),
            output_filename="ow-gebiedsaanwijzingen.xml",
        )
