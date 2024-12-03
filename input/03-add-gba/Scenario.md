# 03 Mutation Add Gebiedsaanwijzingen

## scenario
- new act expression of 02-mutation scenario (omgevingsvisie-1-2)
- mutate existing policy text content to add gba tags

## package data description
Bill: new work omgevingsvisie-1-3 expression version 1
Act: existing work omgevingsvisie-1 expression version 3
Procedure: Final
Opdracht type: Publicatie
Mutation: VervangRegeling

## state change description
New:
    - beleidskeuze-5
        gebiedsaanwijzing-locatie -> werkingsgebied-3 (type lucht)
Mutations:
    - beleidskeuze-1 text added gba
        gebiedsaanwijzing-locatie -> werkingsgebied-1 (type bodem)
Terminations:

## OW state expected changes
New:
    - OWGebiedsaanwijzing -> OWgebiedengroep werkingsgebied-3
    - OWGebiedsaanwijzing -> OWgebiedengroep werkingsgebied-1
    - OWGebiedsaanwijzing -> OWgebiedengroep werkingsgebied-4
    - OWDivisie + OWTekstdeel beleidskeuze-5 add OWGebiedsaanwijzing
Mutations:
    - OWTekstdeel beleidskeuze-1 changed to add OWGebiedsaanwijzing wg-1
    - OWTekstdeel beleidskeuze-4 changed to add OWGebiedsaanwijzing wg-4
Terminations:
