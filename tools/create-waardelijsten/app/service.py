import io
from pathlib import Path
from typing import List
import zipfile
import requests

from config import (
    DOWNLOAD_URL,
    OMGEVINGSVISIE_GA_MATRIX,
    PROGRAMMA_GA_MATRIX,
    SOURCE_FILE,
    TARGET_FILE,
    VAR_NAME_GA_OMGEVINGSVISIE_DATA,
    VAR_NAME_GA_PROGRAMMA_DATA,
)
from source_models import SourceResult, Waardelijst


OUTPUT_FILE_HEADING = """
# GENERATED FILE - DO NOT EDIT

from typing import List
from dso.services.ow.gebiedsaanwijzing.types import Gebiedsaanwijzing, GebiedsaanwijzingGroep, GebiedsaanwijzingType, Waarde
"""


def _download_source() -> SourceResult:
    resp = requests.get(DOWNLOAD_URL)
    resp.raise_for_status()
    zip_bytes = io.BytesIO(resp.content)

    with zipfile.ZipFile(zip_bytes, "r") as z:
        with z.open(SOURCE_FILE) as f:
            return SourceResult.model_validate_json(f.read())


def do_create_gebiedsaanwijzingen():
    output_contents: List[str] = []
    output_contents.append(OUTPUT_FILE_HEADING)

    omgevingsvisie_data_var_names: List[str] = []
    programma_data_var_names: List[str] = []

    source: SourceResult = _download_source()
    gebiedsaanwijzing_type: Waardelijst = source.get_by_label("type gebiedsaanwijzing")
    for type_waarde in gebiedsaanwijzing_type.waarden.waarde:
        waarde_groep: Waardelijst = source.get_by_domein(type_waarde.label)

        waardes_output: List[str] = []
        for waarde in waarde_groep.waarden.waarde:
            waardes_output.append(f"""
                Waarde(
                    label="{waarde.label}",
                    term="{waarde.term}",
                    uri="{waarde.uri}",
                    definitie="{waarde.definitie}",
                    toelichting="{waarde.toelichting}",
                    bron="{waarde.bron}",
                    domain="{waarde.domein}",
                    deprecated={str(waarde.is_deprecated())},
                )""")

        variable_name: str = f"ga_{waarde_groep.get_key()}_groep"
        output_contents.append(f"""
{variable_name} = Gebiedsaanwijzing(
    aanwijzing_type=GebiedsaanwijzingType(
        label="{type_waarde.label}",
        term="{type_waarde.term}",
        uri="{type_waarde.uri}",
        definitie="{type_waarde.definitie}",
        bron="{type_waarde.bron}",
        domein="{type_waarde.domein}",
        deprecated={str(type_waarde.is_deprecated())},
    ),
    aanwijzing_groep=GebiedsaanwijzingGroep(
        label="{waarde_groep.label}",
        titel="{waarde_groep.titel}",
        uri="{waarde_groep.uri}",
        omschrijving="{waarde_groep.omschrijving}",
        toelichting="{waarde_groep.toelichting}",
    ),
    waardes=[
        {",\n\t\t\t".join(waardes_output)}
    ]
)
""")

        if type_waarde.label in OMGEVINGSVISIE_GA_MATRIX:
            omgevingsvisie_data_var_names.append(variable_name)
        if type_waarde.label in PROGRAMMA_GA_MATRIX:
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
            f"We are missing these waardelijsten `{', '.join(set(OMGEVINGSVISIE_GA_MATRIX) - set(omgevingsvisie_data_var_names))}` for Ongevingsvisie"
        )
    if len(programma_data_var_names) != len(PROGRAMMA_GA_MATRIX):
        raise RuntimeError(
            f"We are missing these waardelijsten `{', '.join(set(PROGRAMMA_GA_MATRIX) - set(programma_data_var_names))}` for Programma"
        )

    final_output_contents: str = "\n\n".join(output_contents)
    target_path = Path("../../") / TARGET_FILE
    resolved_path = target_path.resolve()

    with open(resolved_path, "w", encoding="utf-8") as f:
        f.write(final_output_contents)

    print("Done!")
