from typing import Set

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
    ambtsgebieden: Set[OwAmbtsgebied] = Field(default_factory=set)
    regelingsgebieden: Set[OwRegelingsgebied] = Field(default_factory=set)
    gebieden: Set[OwGebied] = Field(default_factory=set)
    gebiedengroepen: Set[OwGebiedengroep] = Field(default_factory=set)
    gebiedsaanwijzingen: Set[OwGebiedsaanwijzing] = Field(default_factory=set)
    divisies: Set[OwDivisie] = Field(default_factory=set)
    divisieteksten: Set[OwDivisietekst] = Field(default_factory=set)
    tekstdelen: Set[OwTekstdeel] = Field(default_factory=set)
