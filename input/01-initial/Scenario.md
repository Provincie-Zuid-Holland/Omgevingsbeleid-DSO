# 01 Initial act template omgevingsvisie 

## scenario
- besluit containing initial omgevingsdocument type omgevingsvisie
- new act work/expression
- no existing state for Acts, EWIDS, GIO's, OWObjects
- new policy objects and werkingsgebieden created as RegelingVrijetekst and GIO's.
- Object templates provided for:
    - visie_algemeen
    - ambitie
    - beleidsdoel
    - beleidskeuze (has gebied-code annotation)
- new asset provided to convert from tekst hint
- new OW state created for types:
    - owgebied(groepen)
    - owdivisie(tekst) + owtekstdelen
    - owgebiedsaanwijzingen
    - owambtsgebied + owregelingsgebied


## package data description
Bill: new work omgevingsvisie-1 expression version 1
Act: new work omgevingsvisie-1 expression version 1
Procedure: Final
Opdracht type: Publicatie
Mutation: No

## state change description

New:
    - Visie Algemeen 1
    - Visie Algemeen 2
    - Ambitie 1
    - Ambitie 2
    - Beleidsdoel 1
    - Beleidskeuze 1
        gebied code: werkingsgebied-1
    - Beleidskeuze 2
        gebied code: werkingsgebied-2
    - Beleidskeuze 3
        gebied code: null (ambtsgebied)
    - Werkingsgebied 1
    - Werkingsgebied 2
    - Ambtsgebied

Mutations:
    - none
 
Terminations:
    - none

## OW state expected changes

New:
    - OWAmbtsgebied
    - OWRegelingsgebied -> Ambtsgebied
    - OWGebied + OWGebiedengroep Testgebied 1
    - OWGebied + OWGebiedengroep Testgebied 2
    - OWDivisie + OWTekstdeel beleidskeuze-1 -> Testgebied 1
    - OWDivisie + OWTekstdeel beleidskeuze-2 -> Testgebied 2
    - OWDivisie + OWTekstdeel beleidskeuze-3 -> Ambtsgebied

Mutations:
    - none

Terminations:
    - none
