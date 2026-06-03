from typing import List

from .registry import WaardelijstProcessor
from .source_models import SourceResult, Waarde, Waardelijst

OUTPUT_FILE_HEADING = """
# GENERATED FILE - DO NOT EDIT

from typing import Dict
from dso.services.ow.themas.types import Thema
"""


class ThemaProcessor(WaardelijstProcessor):
    def process(self, source: SourceResult) -> str:
        output_contents: List[str] = [OUTPUT_FILE_HEADING]

        thema_list: Waardelijst = source.get_by_label("thema")

        themas: List[Waarde] = thema_list.waarden.waarde
        if themas:
            output_contents.append("themas: Dict[str, Thema] = {\n")

        for thema_type in thema_list.waarden.waarde:
            output_contents.append(f"""
    "{thema_type.label}":
    Thema(
        label="{thema_type.label}",
        term="{thema_type.term}",
        uri="{thema_type.uri}",
        definitie="{thema_type.definitie}",
        toelichting="{thema_type.toelichting}",
        bron="{thema_type.bron}",
        domein="{thema_type.domein}",
        deprecated={str(thema_type.is_deprecated())},
    ),""")
        if themas:
            output_contents.append("}\n")

        result: str = "\n\n".join(output_contents)
        return result
