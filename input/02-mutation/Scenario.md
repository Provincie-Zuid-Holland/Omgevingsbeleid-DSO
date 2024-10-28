# 02 Mutation

## scenario
- new act expression of 01-initial scenario (omgevingsvisie-1-1)
- mutation of policy objects
- intrekking GIOs
- mutating and terminating OW objs


## package data description
Bill: new work omgevingsvisie-1 expression version 1
Act: new work omgevingsvisie-1 expression version 1
Procedure: Final
Opdracht type: Publicatie
Mutation: VervangRegeling ()

## state change description
New:
    - Werkingsgebied 3
    - Beleidskeuze 4
        gebied code: wg-3
Mutations:
    - beleidskeuze-1
        gebied code -> ambtsgebied
    - beleidskeuze-3
        gebied code ambtsgebied -> werkingsgebied 1
Terminations:
    - beleidskeuze-2
        werkingsgebied-2 (GIO + OW)

## OW state expected changes
New:
    - OWGebied + OWGebiedengroep Testgebied 3
    - OWDivisie + OWTekstdeel beleidskeuze-4
Mutations:
    - OWTekstdeel beleidskeuze-1
    - OWTekstdeel beleidskeuze-3
Terminations:
    - OWGebied + OWGebiedengroep Testgebied 2
    - OWDivisie + OWTekstdeel beleidskeuze-2
