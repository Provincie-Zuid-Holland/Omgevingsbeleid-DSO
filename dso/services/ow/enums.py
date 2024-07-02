from enum import Enum

# Type spec of IMOW


class IMOWTYPES(str, Enum):
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


class OwLocatieObjectType(str, Enum):
    AMBTSGEBIED = "Ambtsgebied"
    GEBIED = "Gebied"
    GEBIEDENGROEP = "Gebiedengroep"


class OwDivisieObjectType(str, Enum):
    DIVISIE = "Divisie"
    DIVISIETEKST = "Divisietekst"
    TEKSTDEEL = "Tekstdeel"


class OwRegelingsgebiedObjectType(str, Enum):
    REGELINGSGEBIED = "Regelingsgebied"


class OwProcedureStatus(str, Enum):
    """
    For OW objects the procedure status is not provided by default (for "Definitief")
    and only the value "ontwerp" is added for ontwerp besluiten.
    """

    ONTWERP = "ontwerp"


class OwObjectStatus(str, Enum):
    """
    No status == active, "beëindigen" == terminated
    """

    BEEINDIG = "beëindigen"
