# 02-2 Alternative Mutation scenario Omgevingsvisie

Tests an updated state without new or mutated OWLocaties and OWDivisies.
Hardcoded werkingsgebieden.json uuid to make sure no Gebied is mutated:
"d192ed4d-400a-4c5c-9c8d-e274feb0deca" to: 00000000-0000-0005-0000-000000000001

## simulated input from api fixture data
- module_ID: 3
- version_uuid: 1851661a874e4d19acad2867c1125d9a

## changes

module_obj_context:
- Edit beleidskeuze-1 Title

# Expected OW state
Expect complete output without OWfiles.
manifest-ow is required, but should contain no <bestand> entries

New: 0
    - none

Mutations: 0
    - none

Terminations: 0 
    - none

