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


class OwProcedureStatus(Enum):
    """
    For OW objects the procedure status is not provided by default (for "Definitief")
    and only the value "ontwerp" is added for ontwerp besluiten.
    Source: IMOW 2.0.2
    """

    ONTWERP = "ontwerp"
