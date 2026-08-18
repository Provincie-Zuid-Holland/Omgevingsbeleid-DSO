from pydantic import BaseModel, Field

from dso.act_builder.services.ow.state.models import (
    OwAmbtsgebied,
    OwDivisie,
    OwDivisietekst,
    OwGebied,
    OwGebiedengroep,
    OwGebiedsaanwijzing,
    OwRegelingsgebied,
    OwTekstdeel,
)


class OwState(BaseModel):
    ambtsgebieden: set[OwAmbtsgebied] = Field(default_factory=set)
    regelingsgebieden: set[OwRegelingsgebied] = Field(default_factory=set)
    gebieden: set[OwGebied] = Field(default_factory=set)
    gebiedengroepen: set[OwGebiedengroep] = Field(default_factory=set)
    gebiedsaanwijzingen: set[OwGebiedsaanwijzing] = Field(default_factory=set)
    divisies: set[OwDivisie] = Field(default_factory=set)
    divisieteksten: set[OwDivisietekst] = Field(default_factory=set)
    tekstdelen: set[OwTekstdeel] = Field(default_factory=set)
