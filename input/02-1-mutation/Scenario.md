# 02-mutation scenario
Continues from initial state

main.json - OLD OWdata model from api environment state
updated_owdata.json - Same config but using V2 full OwData objects

## simulated input
- module_ID: 2
- version_uuid: f80392dc-6e9a-4054-98ef-6c2f99f359ab

## changes

module_obj_context:
- new werkingsgebied: werkingsgebied-2
- new beleidskeuze-3 - annotation: werkingsgebied-2
- edit beleidskeuze 1: swap geo from werkingsgebied-1 to new werkingsgebied-2
- deleted beleidskeuze 2 (annotated to werkingsgebied 1)

# Expected OW state

New:
    - OWGebied wg2 (werkingsgebied-2)
    - OWGebiedenGroep wg2 (werkingsgebied-2)
    - OWdivisietekst bk-3
    - OWTekstdeel (OWGebiedengroep wg-2 + OWdivisietekst bk-3)

Mutations:
    - OWTekstdeel bk-1 <-> wg1: change locatieref to new OWGebiedenGroep wg2
 
 Terminations:
    - OWDivisietekst (bk-2)
    - OWTekstdeel (bk-2 <-> wg-1)
    - OWGebied + OWGebiedengroep wg-1
