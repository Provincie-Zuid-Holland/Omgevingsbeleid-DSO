# 02-1 Mutation scenario Omgevingsvisie
After initial state for act was created, this scenario mocks some new policy objects / mutations to existing objects and OW terminations.

## simulated input from api fixture data
- module_ID: 2
- version_uuid: 3e0af676582d47ae8bedd43f4e32e748

## changes

module_obj_context:
- new werkingsgebied: werkingsgebied-2: Harkgebied
- new beleidskeuze-3 - annotation: werkingsgebied-2
- edit beleidskeuze-1 werkingsgebied to "werkingsgebied-2"
- terminate beleidskeuze-2

# Expected OW state

New: 4 OW objects
    - OWGebied (werkingsgebied-2)
    - OWGebiedenGroep (werkingsgebied-2)
    - OWdivisietekst beleidskeuze-3: 'pv28_3__div_o_2__div_o_1__div_o_1__content_o_1'
    - OWTekstdeel (OWGebiedengroep wg-2 + OWDivisietekst bk-3)

Mutations: 1 OW obj
    - OWTekstdeel (OWDivisietekst bk-1) updated locaties to Gebiedengroep WG-2
 
Terminations: 4 OW objects (bk-2 and wg-1)
    - OWGebied (werkingsgebied-1)
    - OWGebiedenGroep (werkingsgebied-1)
    - OWdivisietekst beleidskeuze-2: ''pv28_2__div_o_2__div_o_1__div_o_1__content_o_2''
    - OWTekstdeel (OWGebiedengroep wg-1 + OWDivisietekst bk-2)
