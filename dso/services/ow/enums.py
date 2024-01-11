from enum import Enum


class IMOWTYPES(Enum):
    REGELTEKST = "regeltekst"
    GEBIED = "gebied"
    GEBIEDENGROEP = "gebiedengroep"
    LIJN = "lijn"
    LIJNENGROEP = "lijnengroep"
    PUNT = "punt"
    PUNTENGROEP = "puntengroep"
    ACTIVITEIT = "activiteit"
    GEBIEDSAANWIJZING = "gebiedsaanwijzing"
    OMGEVINGSWAARDE = "omgevingswaarde"
    OMGEVINGSNORM = "omgevingsnorm"
    PONS = "pons"
    KAART = "kaart"
    TEKSTDEEL = "tekstdeel"
    HOOFDLIJN = "hoofdlijn"
    DIVISIE = "divisie"
    KAARTLAAG = "kaartlaag"
    JURIDISCHEREGEL = "juridischeregel"
    ACTIVITEITLOCATIEAANDUIDING = "activiteitlocatieaanduiding"
    NORMWAARDE = "normwaarde"
    REGELINGSGEBIED = "regelingsgebied"
    AMBTSGEBIED = "ambtsgebied"
    DIVISIETEKST = "divisietekst"


class OwLocatieObjectType(Enum):
    AMBTSGEBIED = "Ambtsgebied"
    GEBIED = "Gebied"
    GEBIEDENGROEP = "Gebiedengroep"


class OwDivisieObjectType(Enum):
    DIVISIE = "Divisie"
    DIVISIETEKST = "Divisietekst"
    TEKSTDEEL = "Tekstdeel"


class OwRegelingsgebiedObjectType(Enum):
    REGELINGSGEBIED = "Regelingsgebied"
