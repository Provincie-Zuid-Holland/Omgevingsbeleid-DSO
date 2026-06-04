from typing import List

from .config import (
    OMGEVINGSVISIE_GA_MATRIX,
    PROGRAMMA_GA_MATRIX,
    VAR_NAME_GA_OMGEVINGSVISIE_DATA,
    VAR_NAME_GA_PROGRAMMA_DATA,
)
from .registry import WaardelijstProcessor
from .source_models import SourceResult, Waardelijst

OUTPUT_FILE_HEADING = """
# GENERATED FILE - DO NOT EDIT

from typing import List
from dso.services.ow.gebiedsaanwijzingen.types import GebiedsaanwijzingWaarde, GebiedsaanwijzingType, GebiedsaanwijzingGroep, Gebiedsaanwijzing
"""


class GebiedsaanwijzingProcessor(WaardelijstProcessor):
    """
    The values of this waardelijst point to other waardelijsten which can be used in Area of Designations.

    So first we need to fetch the `type gebiedsaanwijzing` waardelijst.
    Then iterate over those values and parse the targeted waardelijsten as Area of Designations.

    And finally we build these sets for each Document Type as not all document types allow us
    to use all Area of Designations. We configure those in the config.
    """

    def process(self, source: SourceResult) -> str:
        output_contents: List[str] = [OUTPUT_FILE_HEADING]

        omgevingsvisie_data_var_names: List[str] = []
        programma_data_var_names: List[str] = []

        designation_type_list: Waardelijst = source.get_by_label("type gebiedsaanwijzing")
        for designation_type in designation_type_list.waarden.waarde:
            designation_group: Waardelijst = source.get_by_domain(designation_type.label)

            values_output: List[str] = []
            for value in designation_group.waarden.waarde:
                values_output.append(f"""
        GebiedsaanwijzingWaarde(
            label="{value.label}",
            term="{value.term}",
            uri="{value.uri}",
            definitie="{value.definitie}",
            toelichting="{value.toelichting}",
            bron="{value.bron}",
            domein="{value.domein}",
            deprecated={str(value.is_deprecated())},
        )""")

            variable_name: str = f"ga_{designation_group.get_key()}_groep"
            output_contents.append(f"""
{variable_name} = Gebiedsaanwijzing(
    aanwijzing_type=GebiedsaanwijzingType(
        label="{designation_type.label}",
        term="{designation_type.term}",
        uri="{designation_type.uri}",
        definitie="{designation_type.definitie}",
        bron="{designation_type.bron}",
        domein="{designation_type.domein}",
        deprecated={str(designation_type.is_deprecated())},
    ),
    aanwijzing_groep=GebiedsaanwijzingGroep(
        label="{designation_group.label}",
        titel="{designation_group.titel}",
        uri="{designation_group.uri}",
        omschrijving="{designation_group.omschrijving}",
        toelichting="{designation_group.toelichting}",
    ),
    waardes=[
        {",\n\t\t\t".join(values_output)}
    ]
)
        """)

            if designation_type.label in OMGEVINGSVISIE_GA_MATRIX:
                omgevingsvisie_data_var_names.append(variable_name)
            if designation_type.label in PROGRAMMA_GA_MATRIX:
                programma_data_var_names.append(variable_name)

        output_contents.append(f"""
{VAR_NAME_GA_OMGEVINGSVISIE_DATA}: List[Gebiedsaanwijzing] = [
    {",\n\t".join(omgevingsvisie_data_var_names)}
]
""")

        output_contents.append(f"""
{VAR_NAME_GA_PROGRAMMA_DATA}: List[Gebiedsaanwijzing] = [
    {",\n\t".join(programma_data_var_names)}
]
""")

        if len(omgevingsvisie_data_var_names) != len(OMGEVINGSVISIE_GA_MATRIX):
            raise RuntimeError(
                f"We are missing these value lists `{', '.join(set(OMGEVINGSVISIE_GA_MATRIX) - set(omgevingsvisie_data_var_names))}` for Ongevingsvisie"
            )
        if len(programma_data_var_names) != len(PROGRAMMA_GA_MATRIX):
            raise RuntimeError(
                f"We are missing these value lists `{', '.join(set(PROGRAMMA_GA_MATRIX) - set(programma_data_var_names))}` for Programma"
            )

        result: str = "\n\n".join(output_contents)
        return result
