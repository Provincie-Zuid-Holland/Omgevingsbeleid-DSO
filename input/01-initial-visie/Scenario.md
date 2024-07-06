# 01 Initial load Omgevingsvisie mock scenario
Initial load Omgevingsvisie mock scenario, create a final publication without prior state.

## simulated input
using mock data from app/tests/database_fixtures_publications.py

- module_ID: 1
- version_uuid: 90000006-0000-0000-0000-000000000003

## changes

module_obj_context:
- new werkingsgebied: werkingsgebied-1: Maatwerkgebied glastuinbouw
- new ambitie-1
- new ambitie-3
- new ambitie-4
- new ambitie-5
- new beleidsdoel-1 
- new beleidsdoel-2 
- new beleidskeuze-1 - annotation: werkingsgebied-1
- new beleidskeuze-2 - annotation: werkingsgebied-1
- visie_algemeen-1
- visie_algemeen-2

# Expected OW state

New:
    - OWGebied (werkingsgebied-2)
    - OWGebiedenGroep (werkingsgebied-2)
    - OWdivisietekst beleidskeuze-1
    - OWdivisietekst beleidskeuze-2
    - OWTekstdeel (OWGebiedengroep wg-1 + OWDivisietekst bk-1)
    - OWTekstdeel (OWGebiedengroep wg-1 + OWDivisietekst bk-2)

Mutations:
    - none
 
Terminations:
    - none
