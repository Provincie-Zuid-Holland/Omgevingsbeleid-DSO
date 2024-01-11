import re
from uuid import uuid4

from .enums import IMOWTYPES

OW_REGEX = r"nl\.imow-(gm|pv|ws|mn|mnre)[0-9]{1,6}\.(regeltekst|gebied|gebiedengroep|lijn|lijnengroep|punt|puntengroep|activiteit|gebiedsaanwijzing|omgevingswaarde|omgevingsnorm|pons|kaart|tekstdeel|hoofdlijn|divisie|kaartlaag|juridischeregel|activiteitlocatieaanduiding|normwaarde|regelingsgebied|ambtsgebied|divisietekst)\.[A-Za-z0-9]{1,32}"


def generate_ow_id(ow_type: IMOWTYPES, organisation_id: str = "pv28"):
    prefix = f"nl.imow-{organisation_id}"
    unique_code = uuid4()
    generated_id = f"{prefix}.{ow_type.value}.{unique_code.hex}"

    imow_pattern = re.compile(OW_REGEX)
    if not imow_pattern.match(generated_id):
        raise Exception("generated IMOW ID does not match official regex")

    return generated_id
