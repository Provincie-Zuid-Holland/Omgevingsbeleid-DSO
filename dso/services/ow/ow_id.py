import re
from typing import Optional
from uuid import uuid4

from .enums import IMOWTYPES

OW_REGEX = r"nl\.imow-(gm|pv|ws|mn|mnre)[0-9]{1,6}\.(regeltekst|gebied|gebiedengroep|lijn|lijnengroep|punt|puntengroep|activiteit|gebiedsaanwijzing|omgevingswaarde|omgevingsnorm|pons|kaart|tekstdeel|hoofdlijn|divisie|kaartlaag|juridischeregel|activiteitlocatieaanduiding|normwaarde|regelingsgebied|ambtsgebied|divisietekst)\.[A-Za-z0-9]{1,32}"


def generate_ow_id(ow_type: IMOWTYPES, organisation_id: str = "pv28", unique_code: Optional[str] = None):
    prefix = f"nl.imow-{organisation_id}"
    if not unique_code:
        unique_code = uuid4().hex

    generated_id = f"{prefix}.{ow_type.value}.{unique_code}"

    imow_pattern = re.compile(OW_REGEX)
    if not imow_pattern.match(generated_id):
        raise ValueError(f"Generated IMOW ID: '{generated_id}' does not match official regex")

    return generated_id


def check_ow_id_imowtype(ow_id: str) -> IMOWTYPES:
    imow_pattern = re.compile(OW_REGEX)
    if not imow_pattern.match(ow_id):
        raise ValueError(f"Provided ow_id: '{ow_id}' does not match ow_regex pattern")

    try:
        imow_type = IMOWTYPES(ow_id.split(".")[2])
    except ValueError as e:
        raise ValueError(f"Invalid IMOWTYPES value in ow_id: '{ow_id}'. Error: {str(e)}")

    return imow_type
