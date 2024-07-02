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
        'nl.imow-pv28.tekstdeel.bb7264bf2df541c997f548f61daa3b45'
 
 Terminations:
    - OWDivisietekst (bk-2)
        'nl.imow-pv28.divisietekst.b6bce5badb1c43ab9a5acd5918dec8ec'
    - OWTekstdeel (bk-2 <-> wg-1)
        'nl.imow-pv28.tekstdeel.b701ed96086548f3a3422f9e54501161'
    - OWGebied + OWGebiedengroep wg-1 
        nl.imow-pv28.gebiedengroep.e1adff3019b84520a9dfa4fa358a852f
        nl.imow-pv28.gebied.660de48c96634921b95fd040ea8625b5
