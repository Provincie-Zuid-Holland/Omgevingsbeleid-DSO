from typing import List, Optional

from .waardelijsten import (
    BEPERKINGENGEBIEDGROEP_VALUES,
    BODEMGROEP_VALUES,
    BOUWGROEP_VALUES,
    DEFENSIEGROEP_VALUES,
    ENERGIEVOORZIENINGGROEP_VALUES,
    ERFGOEDGROEP_VALUES,
    EXTERNE_VEILIGHEIDGROEP_VALUES,
    FUNCTIEGROEP_VALUES,
    GELUIDGROEP_VALUES,
    GEURGROEP_VALUES,
    LEIDINGGROEP_VALUES,
    LUCHTGROEP_VALUES,
    MIJNBOUWGROEP_VALUES,
    NATUURGROEP_VALUES,
    RECREATIEGROEP_VALUES,
    RUIMTELIJK_GEBRUIKGROEP_VALUES,
    VERKEERGROEP_VALUES,
    WATER_EN_WATERSYSTEEMGROEP_VALUES,
    LANDSCHAPGROEP_VALUES,
)

GEBIEDSAANWIJZING_TO_GROEP_MAPPING = {
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Beperkingengebied": BEPERKINGENGEBIEDGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Bodem": BODEMGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Bouw": BOUWGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Defensie": DEFENSIEGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Energievoorziening": ENERGIEVOORZIENINGGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Erfgoed": ERFGOEDGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/ExterneVeiligheid": EXTERNE_VEILIGHEIDGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Functie": FUNCTIEGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Geluid": GELUIDGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Geur": GEURGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Landschap": LANDSCHAPGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Leiding": LEIDINGGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Lucht": LUCHTGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Mijnbouw": MIJNBOUWGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Natuur": NATUURGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Recreatie": RECREATIEGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/RuimtelijkGebruik": RUIMTELIJK_GEBRUIKGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Verkeer": VERKEERGROEP_VALUES,
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/WaterEnWatersysteem": WATER_EN_WATERSYSTEEMGROEP_VALUES,
}

NON_ALLOWED_DOCUMENT_TYPE_MAPPING = {
    "omgevingsvisie": [
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Beperkingengebied",
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Bouw",
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Functie",
    ],
    "programma": [
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Beperkingengebied",
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Bouw",
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Functie",
    ],
}

def get_groep_values_for_gebiedsaanwijzing_type(aanwijzingtype_uri: str) -> Optional[List[str]]:
    groep_value_list = GEBIEDSAANWIJZING_TO_GROEP_MAPPING.get(aanwijzingtype_uri)
    if not groep_value_list:
        return None
    return [entry.uri for entry in groep_value_list.waarden.waarde]

def get_groep_options_for_gebiedsaanwijzing_type(aanwijzingtype_uri: str) -> Optional[List[str]]:
    groep_value_list = GEBIEDSAANWIJZING_TO_GROEP_MAPPING.get(aanwijzingtype_uri)
    if not groep_value_list:
        return None
    return [entry.label for entry in groep_value_list.waarden.waarde]

def is_uri_allowed_for_document_type(doc_type: str, uri: str) -> bool:
    non_allowed = NON_ALLOWED_DOCUMENT_TYPE_MAPPING.get(doc_type, [])
    return uri not in non_allowed