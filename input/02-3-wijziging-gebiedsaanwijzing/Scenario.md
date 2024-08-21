# 02-2 Mutation scenario gebiedsaanwijzingen

## changes

module_obj_context:
- new werkingsgebied: werkingsgebied-2: Harkgebied
- new beleidskeuze-3 - annotation: werkingsgebied-2, 
- new GBA annotation to existing wg-1
- new GBA annotation to wg-2
- terminate beleidskeuze-2

# Expected OW state

New: 4 OW objects
    - OWGebied (werkingsgebied-2)
    - OWGebiedenGroep (werkingsgebied-2)
    - OWdivisietekst beleidskeuze-3: 'pv28_3__div_o_2__div_o_1__div_o_1__content_o_1'
    - OWTekstdeel (OWGebiedengroep wg-2 + OWDivisietekst bk-3)
    - 2x OWGebiedsaanwijzing
        - wg-1
        - wg-2

Mutations: 1 OW obj
    - None
 
Terminations: 4 OW objects (bk-2 and wg-1)
    - OWdivisietekst beleidskeuze-2: ''pv28_2__div_o_2__div_o_1__div_o_1__content_o_2''
    - OWTekstdeel: bk-2. (OWGebiedengroep wg-1 not deleted because used in BK3 GBA)
