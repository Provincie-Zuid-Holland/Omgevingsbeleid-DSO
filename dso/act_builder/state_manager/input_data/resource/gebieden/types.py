import re
from uuid import UUID
from typing import List, Set

from pydantic import BaseModel, ConfigDict

from ......models import GioFRBR


class GioLocatie(BaseModel):
    """
    This represents a Locatie in GeoInformatieObjectVaststelling.vastgesteldeVersie.GeoInformatieObjectVersie.locaties
    From the API's perspective this is the `Area` attached to a `Gebied`
    """

    code: str  # The gebied-x code this locatie represents
    title: str
    basisgeo_id: str
    gml: str


class Gio(BaseModel):
    """
    This represents a AanleveringInformatieObject and GeoInformatieObjectVaststelling
    And all that comes with it, like consolidating and listing it in the Appendix of the Act.

    A Gio can be build by the API's Object_Type=gebied where this Gio will just have
    one `locatie` which is the Area in Gebied.Area_UUID

    And a Gio can be build by an Gebiedsaanwijzing where it might have multiple `locatie`
    """

    # These are the gebied-x codes which are in this gio
    # source_codes and the key() func are used to determine uniquenes and "lineage"
    source_codes: Set[str]  # [gebied-1, gebied-2]
    locaties: List[GioLocatie]  # 1 locatie per source-code

    title: str
    frbr: GioFRBR
    new: bool
    geboorteregeling: str
    achtergrond_verwijzing: str
    achtergrond_actualiteit: str

    def key(self) -> str:
        return "_".join(sorted(self.source_codes))

    def wid_key(self) -> str:
        return "_".join(sorted(self.source_codes))

    def get_name(self) -> str:
        s: str = self.title.lower()
        s = re.sub(r"[^a-z0-9 ]+", "", s)
        s = s.replace(" ", "-")
        return s

    def get_gml_filename(self) -> str:
        return f"locaties_{self.get_name()}.gml"

    def get_gio_filename(self) -> str:
        return f"GIO_locaties_{self.get_name()}.xml"


class GebiedenGroep(BaseModel):
    """
    GebiedenGroep comes from the API Object_Type=gebiedengroep
    Which always point to a Gio which just like it does in the API

    This class will be used for ow.gebiedengroep where it will point to ow.gebied
    Some ow.Tekstdelen will use this ow.gebiedengroep
    This will represent the API.Object.Maatregel.Gebiedengroep configuration
    """

    uuid: UUID
    code: str  # Code used by the API like `gebiedengroep-1`
    title: str
    geo_gio_keys: List[str]

    model_config = ConfigDict(populate_by_name=True)


class Gebiedsaanwijzing(BaseModel):
    uuid: UUID
    aanwijzing_type: str
    aanwijzing_groep: str
    title: str
    source_gebied_codes: Set[str]
    geo_gio_key: str

    def key(self) -> str:
        return "_".join(sorted(self.source_gebied_codes))
