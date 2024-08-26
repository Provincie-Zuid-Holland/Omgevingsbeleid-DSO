from enum import Enum
from typing import List, Optional


class TypeGebiedsaanwijzingEnum(str, Enum):
    """
    Resource: http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/TypeGebiedsaanwijzing_4.0.0
    Version: 4.0.0
    """

    Beperkingengebied = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Beperkingengebied"
    Bodem = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Bodem"
    Bouw = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Bouw"
    Defensie = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Defensie"
    Energievoorziening = (
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Energievoorziening"
    )
    Erfgoed = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Erfgoed"
    ExterneVeiligheid = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/ExterneVeiligheid"
    Functie = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Functie"
    Geluid = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Geluid"
    Geur = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Geur"
    Landschap = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Landschap"
    Leiding = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Leiding"
    Lucht = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Lucht"
    Mijnbouw = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Mijnbouw"
    Natuur = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Natuur"
    Recreatie = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Recreatie"
    RuimtelijkGebruik = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/RuimtelijkGebruik"
    Verkeer = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/Verkeer"
    WaterEnWatersysteem = (
        "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/WaterEnWatersysteem"
    )


class BeperkingengebiedGroepEnum(str, Enum):
    InstallatieInWaterstaatswerk = (
        "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/InstallatieInWaterstaatswerk"
    )
    Luchthaven = "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/Luchthaven"
    Molen = "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/Molen"
    Overig = "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/Overig"
    Spoorweg = "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/Spoorweg"
    Waterstaatswerk = "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/Waterstaatswerk"
    Weg = "http://standaarden.omgevingswet.overheid.nl/beperkingengebied/id/concept/Weg"


class BodemGroepEnum(str, Enum):
    Bodembeheergebied = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/Bodembeheergebied"
    Bodemdalingsgebied = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/Bodemdalingsgebied"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/Maatregelengebied"
    Mijnsteengebied = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/Mijnsteengebied"
    Ontgrondingsgebied = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/Ontgrondingsgebied"
    StortplaatsGesloten = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/StortplaatsGesloten"
    StortplaatsOpen = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/StortplaatsOpen"
    Zandwinningsgebied = "http://standaarden.omgevingswet.overheid.nl/bodem/id/concept/Zandwinningsgebied"


class BouwGroepEnum(str, Enum):
    Bouwvlak = "http://standaarden.omgevingswet.overheid.nl/bouw/id/concept/Bouwvlak"
    NietGeluidgevoeligeGevel = "http://standaarden.omgevingswet.overheid.nl/bouw/id/concept/NietGeluidgevoeligeGevel"
    Rooilijn = "http://standaarden.omgevingswet.overheid.nl/bouw/id/concept/Rooilijn"


class DefensieGroepEnum(str, Enum):
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/defensie/id/concept/Maatregelengebied"
    MilitaireLaagvliegroute = "http://standaarden.omgevingswet.overheid.nl/defensie/id/concept/MilitaireLaagvliegroute"
    MilitairTerrein = "http://standaarden.omgevingswet.overheid.nl/defensie/id/concept/MilitairTerrein"
    Radarverstoringsgebied = "http://standaarden.omgevingswet.overheid.nl/defensie/id/concept/Radarverstoringsgebied"
    VerstoringsgebiedMilitaireZendEnOntvangstinstallatie = "http://standaarden.omgevingswet.overheid.nl/defensie/id/concept/VerstoringsgebiedMilitaireZendEnOntvangstinstallatie"


class EnergievoorzieningGroepEnum(str, Enum):
    Bodemenergiegebied = "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/Bodemenergiegebied"
    Energieproductiegebied = (
        "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/Energieproductiegebied"
    )
    GrootschaligeElektriciteitsopwekking = (
        "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/GrootschaligeElektriciteitsopwekking"
    )
    Hoogspanningsverbinding = (
        "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/Hoogspanningsverbinding"
    )
    Kernenergiegebied = "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/Kernenergiegebied"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/Maatregelengebied"
    Windturbinegebied = "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/Windturbinegebied"
    ZonneEnergiegebied = "http://standaarden.omgevingswet.overheid.nl/energievoorziening/id/concept/ZonneEnergiegebied"


class ErfgoedGroepEnum(str, Enum):
    AardkundigWaardevolGebied = (
        "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/AardkundigWaardevolGebied"
    )
    Archeologie = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/Archeologie"
    BeschermdMonument = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/BeschermdMonument"
    Buitenplaats = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/Buitenplaats"
    CultureelErfgoed = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/CultureelErfgoed"
    CultuurhistorischBeschermdLandschap = (
        "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/CultuurhistorischBeschermdLandschap"
    )
    CultuurhistorischWaardevolGebied = (
        "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/CultuurhistorischWaardevolGebied"
    )
    Linie = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/Linie"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/Maatregelengebied"
    Werelderfgoed = "http://standaarden.omgevingswet.overheid.nl/erfgoed/id/concept/Werelderfgoed"


class ExterneVeiligheidGroepEnum(str, Enum):
    AandachtsgebiedExterneVeiligheid = (
        "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/AandachtsgebiedExterneVeiligheid"
    )
    BelemmeringengebiedBuisleidingen = (
        "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/BelemmeringengebiedBuisleidingen"
    )
    GebiedMetOntplofbareStoffenEnExplosieven = "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/GebiedMetOntplofbareStoffenEnExplosieven"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/Maatregelengebied"
    PlaatsgebondenRisico = (
        "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/PlaatsgebondenRisico"
    )
    Risicogebied = "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/Risicogebied"
    Voorschriftengebied = "http://standaarden.omgevingswet.overheid.nl/externeveiligheid/id/concept/Voorschriftengebied"


class FunctieGroepEnum(str, Enum):
    Aandachtsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Aandachtsgebied"
    AandachtsgebiedExterneVeiligheid = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/AandachtsgebiedExterneVeiligheid"
    )
    AandachtsgebiedGeluid = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/AandachtsgebiedGeluid"
    AandachtsgebiedLuchtkwaliteit = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/AandachtsgebiedLuchtkwaliteit"
    )
    AardkundigeWaarde = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/AardkundigeWaarde"
    Agrarisch = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Agrarisch"
    Archeologie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Archeologie"
    Bebouwingscontour = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Bebouwingscontour"
    BebouwingscontourHoutkap = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/BebouwingscontourHoutkap"
    BebouwingscontourJacht = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/BebouwingscontourJacht"
    Bedrijf = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Bedrijf"
    Bedrijventerrein = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Bedrijventerrein"
    Belemmeringengebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Belemmeringengebied"
    BeschermdeBoom = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/BeschermdeBoom"
    BeschermdGezicht = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/BeschermdGezicht"
    BeschermdLandschap = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/BeschermdLandschap"
    BeschermdMonument = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/BeschermdMonument"
    Bodembeheergebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Bodembeheergebied"
    Bodemdalingsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Bodemdalingsgebied"
    Bodemenergiegebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Bodemenergiegebied"
    Buitenplaats = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Buitenplaats"
    Centrumgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Centrumgebied"
    Concentratiegebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Concentratiegebied"
    Cultuur = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Cultuur"
    CultuurhistorischBeschermdLandschap = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/CultuurhistorischBeschermdLandschap"
    )
    CultuurhistorischWaardevolGebied = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/CultuurhistorischWaardevolGebied"
    )
    Dagrecreatie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Dagrecreatie"
    Detailhandel = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Detailhandel"
    Dienstverlening = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Dienstverlening"
    Duingebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Duingebied"
    Duinwatergebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Duinwatergebied"
    Energieproductiegebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Energieproductiegebied"
    Erfgoed = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Erfgoed"
    Gaswinning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Gaswinning"
    GeslotenStortplaats = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/GeslotenStortplaats"
    Glastuinbouw = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Glastuinbouw"
    Groen = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Groen"
    Grondwaterbeschermingsgebied = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Grondwaterbeschermingsgebied"
    )
    GrootschaligeElektriciteitsopwekking = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/GrootschaligeElektriciteitsopwekking"
    )
    Herstructureringsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Herstructureringsgebied"
    Hoogspanningsverbinding = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Hoogspanningsverbinding"
    Horeca = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Horeca"
    Industrie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Industrie"
    Industrieterrein = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Industrieterrein"
    Infrastructuur = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Infrastructuur"
    Intrekgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Intrekgebied"
    Kantoor = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Kantoor"
    Kantoorlocatie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Kantoorlocatie"
    Kostenverhaalsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Kostenverhaalsgebied"
    Landbouw = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Landbouw"
    LandelijkGebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/LandelijkGebied"
    Luchthaven = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Luchthaven"
    Luchtvaart = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Luchtvaart"
    Maatschappelijk = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Maatschappelijk"
    Mergelwinning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Mergelwinning"
    MilitaireLaagvliegroute = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/MilitaireLaagvliegroute"
    MilitairTerrein = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/MilitairTerrein"
    Moderniseringslocatie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Moderniseringslocatie"
    Molen = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Molen"
    Oliewinning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Oliewinning"
    Ontgrondingsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Ontgrondingsgebied"
    Ontspanning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Ontspanning"
    OntwikkelingLandelijkeFuncties = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/OntwikkelingLandelijkeFuncties"
    )
    OntwikkelingStedelijkeFuncties = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/OntwikkelingStedelijkeFuncties"
    )
    OpenbaarGebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/OpenbaarGebied"
    OpenLandschap = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/OpenLandschap"
    OpenStortplaats = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/OpenStortplaats"
    Overig = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Overig"
    Radarverstoringsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Radarverstoringsgebied"
    Recreatie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Recreatie"
    RecreatiefRoutenetwerk = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/RecreatiefRoutenetwerk"
    Reserveringsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Reserveringsgebied"
    RisicogebiedExterneVeiligheid = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/RisicogebiedExterneVeiligheid"
    )
    Schaliegaswinning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Schaliegaswinning"
    Spoorweg = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Spoorweg"
    Sport = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Sport"
    StedelijkGebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StedelijkGebied"
    StedelijkGebiedBuitenCentrum = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StedelijkGebiedBuitenCentrum"
    )
    StedelijkGebiedCentrumDorps = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StedelijkGebiedCentrumDorps"
    )
    StedelijkGebiedCentrumStedelijk = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StedelijkGebiedCentrumStedelijk"
    )
    StedelijkGebiedGroenStedelijk = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StedelijkGebiedGroenStedelijk"
    )
    StedelijkUitloopgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StedelijkUitloopgebied"
    StilGebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/StilGebied"
    ToepassingsgebiedMijnsteen = (
        "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/ToepassingsgebiedMijnsteen"
    )
    Transformatiegebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Transformatiegebied"
    Veehouderij = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Veehouderij"
    Verblijfsgebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Verblijfsgebied"
    Verblijfsrecreatie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Verblijfsrecreatie"
    Verkeer = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Verkeer"
    VerstoringsgebiedMilitaireZendEnOntvangstinstallatie = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/VerstoringsgebiedMilitaireZendEnOntvangstinstallatie"
    Voorschriftengebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Voorschriftengebied"
    Waarde = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Waarde"
    Water = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Water"
    Waterberging = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Waterberging"
    Waterkering = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Waterkering"
    Waterstaatswerk = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Waterstaatswerk"
    Waterwingebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Waterwingebied"
    Werelderfgoed = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Werelderfgoed"
    Windturbine = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Windturbine"
    Wonen = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Wonen"
    Woongebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Woongebied"
    Zandwinning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Zandwinning"
    ZonneEnergiegebied = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/ZonneEnergiegebied"
    Zoutwinning = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/Zoutwinning"
    ZuiveringtechnischWerk = "http://standaarden.omgevingswet.overheid.nl/functie/id/concept/ZuiveringtechnischWerk"


class GeluidGroepEnum(str, Enum):
    AandachtsgebiedGeluid = "http://standaarden.omgevingswet.overheid.nl/geluid/id/concept/AandachtsgebiedGeluid"
    AgglomeratieRichtlijnOmgevingslawaai = (
        "http://standaarden.omgevingswet.overheid.nl/geluid/id/concept/AgglomeratieRichtlijnOmgevingslawaai"
    )
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/geluid/id/concept/Maatregelengebied"
    Stiltegebied = "http://standaarden.omgevingswet.overheid.nl/geluid/id/concept/Stiltegebied"


class GeurGroepEnum(str, Enum):
    Bebouwingscontour = "http://standaarden.omgevingswet.overheid.nl/geur/id/concept/Bebouwingscontour"
    Concentratiegebied = "http://standaarden.omgevingswet.overheid.nl/geur/id/concept/Concentratiegebied"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/geur/id/concept/Maatregelengebied"


class LandschapGroepEnum(str, Enum):
    BijzonderProvinciaalLandschap = (
        "http://standaarden.omgevingswet.overheid.nl/landschap/id/concept/BijzonderProvinciaalLandschap"
    )
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/landschap/id/concept/Maatregelengebied"
    NationaalLandschap = "http://standaarden.omgevingswet.overheid.nl/landschap/id/concept/NationaalLandschap"
    OpenLandschap = "http://standaarden.omgevingswet.overheid.nl/landschap/id/concept/OpenLandschap"
    SpecifiekBenoemdLandschap = (
        "http://standaarden.omgevingswet.overheid.nl/landschap/id/concept/SpecifiekBenoemdLandschap"
    )


class LeidingGroepEnum(str, Enum):
    Buisleiding = "http://standaarden.omgevingswet.overheid.nl/leiding/id/concept/Buisleiding"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/leiding/id/concept/Maatregelengebied"
    Reserveringsgebied = "http://standaarden.omgevingswet.overheid.nl/leiding/id/concept/Reserveringsgebied"
    TraceHoogspanning = "http://standaarden.omgevingswet.overheid.nl/leiding/id/concept/TraceHoogspanning"


class LuchtGroepEnum(str, Enum):
    AandachtsgebiedLuchtkwaliteit = (
        "http://standaarden.omgevingswet.overheid.nl/lucht/id/concept/AandachtsgebiedLuchtkwaliteit"
    )
    LocatieUitgezonderdVanNibm = (
        "http://standaarden.omgevingswet.overheid.nl/lucht/id/concept/LocatieUitgezonderdVanNibm"
    )
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/lucht/id/concept/Maatregelengebied"
    VarendOntgassen = "http://standaarden.omgevingswet.overheid.nl/lucht/id/concept/VarendOntgassen"


class MijnbouwGroepEnum(str, Enum):
    Algemeen = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Algemeen"
    Gaswinning = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Gaswinning"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Maatregelengebied"
    Mergelwinning = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Mergelwinning"
    Oliewinning = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Oliewinning"
    Schaliegaswinning = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Schaliegaswinning"
    Zoutwinning = "http://standaarden.omgevingswet.overheid.nl/mijnbouw/id/concept/Zoutwinning"


class NatuurGroepEnum(str, Enum):
    BebouwingscontourHoutkap = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/BebouwingscontourHoutkap"
    BebouwingscontourJacht = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/BebouwingscontourJacht"
    BijzonderNationaalNatuurgebied = (
        "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/BijzonderNationaalNatuurgebied"
    )
    BijzonderProvinciaalNatuurgebied = (
        "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/BijzonderProvinciaalNatuurgebied"
    )
    Habitatrichtlijngebied = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/Habitatrichtlijngebied"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/Maatregelengebied"
    NationaalPark = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/NationaalPark"
    Natura2000Gebied = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/Natura2000Gebied"
    Natuurbeheergebied = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/Natuurbeheergebied"
    NatuurnetwerkNederland = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/NatuurnetwerkNederland"
    Toegangsbeperkingsgebied = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/Toegangsbeperkingsgebied"
    Vogelrichtlijngebied = "http://standaarden.omgevingswet.overheid.nl/natuur/id/concept/Vogelrichtlijngebied"


class RecreatieGroepEnum(str, Enum):
    Dagrecreatie = "http://standaarden.omgevingswet.overheid.nl/recreatie/id/concept/Dagrecreatie"
    KleinschaligeVoorzieningen = (
        "http://standaarden.omgevingswet.overheid.nl/recreatie/id/concept/KleinschaligeVoorzieningen"
    )
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/recreatie/id/concept/Maatregelengebied"
    Verblijfsrecreatie = "http://standaarden.omgevingswet.overheid.nl/recreatie/id/concept/Verblijfsrecreatie"


class RuimtelijkGebruikGroepEnum(str, Enum):
    Afvalstoffen = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Afvalstoffen"
    Bebouwingscontour = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Bebouwingscontour"
    Bedrijventerrein = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Bedrijventerrein"
    Detailhandel = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Detailhandel"
    Glastuinbouw = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Glastuinbouw"
    Industrieterrein = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Industrieterrein"
    Infrastructuur = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Infrastructuur"
    Kantoorlocatie = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Kantoorlocatie"
    Landbouw = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Landbouw"
    LandelijkGebied = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/LandelijkGebied"
    LandelijkGebiedAgrarisch = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/LandelijkGebiedAgrarisch"
    )
    LandelijkGebiedHoofdfunctieLandschap = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/LandelijkGebiedHoofdfunctieLandschap"
    )
    LandelijkGebiedHoofdfunctieNatuur = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/LandelijkGebiedHoofdfunctieNatuur"
    )
    LandelijkGebiedStedelijkUitloopgebied = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/LandelijkGebiedStedelijkUitloopgebied"
    )
    LandelijkGebiedVerwevingVanFuncties = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/LandelijkGebiedVerwevingVanFuncties"
    )
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Maatregelengebied"
    OntwikkelingLandelijkeFuncties = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/OntwikkelingLandelijkeFuncties"
    )
    OntwikkelingStedelijkeFuncties = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/OntwikkelingStedelijkeFuncties"
    )
    Overig = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Overig"
    SpecifiekTeeltgebied = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/SpecifiekTeeltgebied"
    )
    StedelijkGebied = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/StedelijkGebied"
    StedelijkGebiedBuitenCentrum = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/StedelijkGebiedBuitenCentrum"
    )
    StedelijkGebiedCentrumDorps = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/StedelijkGebiedCentrumDorps"
    )
    StedelijkGebiedCentrumStedelijk = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/StedelijkGebiedCentrumStedelijk"
    )
    StedelijkGebiedGroenStedelijk = (
        "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/StedelijkGebiedGroenStedelijk"
    )
    Veehouderij = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Veehouderij"
    Water = "http://standaarden.omgevingswet.overheid.nl/ruimtelijkgebruik/id/concept/Water"


class VerkeerGroepEnum(str, Enum):
    Luchtvaart = "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/Luchtvaart"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/Maatregelengebied"
    RecreatieveRoutenetwerken = (
        "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/RecreatieveRoutenetwerken"
    )
    Reserveringsgebied = "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/Reserveringsgebied"
    Spoorweg = "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/Spoorweg"
    Vaarweg = "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/Vaarweg"
    Weg = "http://standaarden.omgevingswet.overheid.nl/verkeer/id/concept/Weg"


class WaterEnWatersysteemGroepEnum(str, Enum):
    Bergingsgebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Bergingsgebied"
    BeschermdeGebieden = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/BeschermdeGebieden"
    BoringsvijeZone = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/BoringsvijeZone"
    Compartimentskering = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Compartimentskering"
    )
    ContourBeregeningsbeleid = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/ContourBeregeningsbeleid"
    )
    Duingebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Duingebied"
    Duinwatergebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Duinwatergebied"
    GebiedsnormWateroverlast = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/GebiedsnormWateroverlast"
    )
    Grondwaterbeschermingsgebied = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Grondwaterbeschermingsgebied"
    )
    Grondwaterdeelgebied = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Grondwaterdeelgebied"
    )
    Intrekgebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Intrekgebied"
    Kade = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Kade"
    Kustfundament = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Kustfundament"
    Maatregelengebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Maatregelengebied"
    Natuurbeek = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Natuurbeek"
    Onderhoudspad = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Onderhoudspad"
    Oppervaktewaterbeschermingsgebied = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Oppervaktewaterbeschermingsgebied"
    )
    Oppervlaktewaterbeheergebied = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Oppervlaktewaterbeheergebied"
    )
    Oppervlaktewaterlichaam = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Oppervlaktewaterlichaam"
    )
    OppervlaktewaterlichaamPrimair = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/OppervlaktewaterlichaamPrimair"
    )
    OppervlaktewaterlichaamProfielVanVrijeRuimte = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/OppervlaktewaterlichaamProfielVanVrijeRuimte"
    OppervlaktewaterlichaamSecundair = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/OppervlaktewaterlichaamSecundair"
    )
    OppervlaktewaterlichaamTertiair = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/OppervlaktewaterlichaamTertiair"
    )
    OverigeGebieden = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/OverigeGebieden"
    Peilgebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Peilgebied"
    Projectgebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Projectgebied"
    Reserveringsgebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Reserveringsgebied"
    SpecifiekBenoemdGebied = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/SpecifiekBenoemdGebied"
    )
    Vaarweg = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Vaarweg"
    Waterberging = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Waterberging"
    Waterkering = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Waterkering"
    WaterkeringOverig = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/WaterkeringOverig"
    WaterkeringPrimair = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/WaterkeringPrimair"
    WaterkeringProfielVanVrijeRuimte = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/WaterkeringProfielVanVrijeRuimte"
    )
    WaterkeringRegionaal = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/WaterkeringRegionaal"
    )
    Waterstaatswerk = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Waterstaatswerk"
    Watersysteem = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Watersysteem"
    Waterwingebied = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Waterwingebied"
    ZuiveringtechnischWerk = (
        "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/ZuiveringtechnischWerk"
    )
    Zwemlocatie = "http://standaarden.omgevingswet.overheid.nl/waterenwatersysteem/id/concept/Zwemlocatie"


GEBIEDSAANWIJZING_TO_GROEP_MAPPING = {
    TypeGebiedsaanwijzingEnum.Beperkingengebied: BeperkingengebiedGroepEnum,
    TypeGebiedsaanwijzingEnum.Bodem: BodemGroepEnum,
    TypeGebiedsaanwijzingEnum.Bouw: BouwGroepEnum,
    TypeGebiedsaanwijzingEnum.Defensie: DefensieGroepEnum,
    TypeGebiedsaanwijzingEnum.Energievoorziening: EnergievoorzieningGroepEnum,
    TypeGebiedsaanwijzingEnum.Erfgoed: ErfgoedGroepEnum,
    TypeGebiedsaanwijzingEnum.ExterneVeiligheid: ExterneVeiligheidGroepEnum,
    TypeGebiedsaanwijzingEnum.Functie: FunctieGroepEnum,
    TypeGebiedsaanwijzingEnum.Geluid: GeluidGroepEnum,
    TypeGebiedsaanwijzingEnum.Geur: GeurGroepEnum,
    TypeGebiedsaanwijzingEnum.Landschap: LandschapGroepEnum,
    TypeGebiedsaanwijzingEnum.Leiding: LeidingGroepEnum,
    TypeGebiedsaanwijzingEnum.Lucht: LuchtGroepEnum,
    TypeGebiedsaanwijzingEnum.Mijnbouw: MijnbouwGroepEnum,
    TypeGebiedsaanwijzingEnum.Natuur: NatuurGroepEnum,
    TypeGebiedsaanwijzingEnum.Recreatie: RecreatieGroepEnum,
    TypeGebiedsaanwijzingEnum.RuimtelijkGebruik: RuimtelijkGebruikGroepEnum,
    TypeGebiedsaanwijzingEnum.Verkeer: VerkeerGroepEnum,
    TypeGebiedsaanwijzingEnum.WaterEnWatersysteem: WaterEnWatersysteemGroepEnum,
}

# Document type matrix from TPOD v3.0.0
# https://docs.geostandaarden.nl/tpod/def-st-TPOD-OVI-20231215/#6F231895
NON_ALLOWED_DOCUMENT_TYPE_MAPPING = {
    "omgevingsvisie": [
        TypeGebiedsaanwijzingEnum.Beperkingengebied,
        TypeGebiedsaanwijzingEnum.Bouw,
        TypeGebiedsaanwijzingEnum.Functie,
    ],
    "programma": [
        TypeGebiedsaanwijzingEnum.Beperkingengebied,
        TypeGebiedsaanwijzingEnum.Bouw,
        TypeGebiedsaanwijzingEnum.Functie,
    ],
}


def get_groep_values_for_gebiedsaanwijzing_type(aanwijzingtype_enum) -> Optional[List[str]]:
    groep_enum = GEBIEDSAANWIJZING_TO_GROEP_MAPPING.get(aanwijzingtype_enum)
    if not groep_enum:
        return None
    return [e.value for e in groep_enum]


def get_groep_options_for_gebiedsaanwijzing_type(aanwijzingtype_enum) -> Optional[List[str]]:
    groep_enum = GEBIEDSAANWIJZING_TO_GROEP_MAPPING.get(aanwijzingtype_enum)
    if not groep_enum:
        return None
    return [e.name for e in groep_enum]
