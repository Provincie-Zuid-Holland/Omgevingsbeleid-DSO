from uuid import UUID

from ...models import OwData, OwDataV1
from .models import (
    BestuurlijkeGrenzenVerwijzing,
    OWAmbtsgebied,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OWRegelingsgebied,
    OWTekstdeel,
)


def migrate_previous_ow_state(known_ow_state_dict: dict) -> OwData:
    """
    Development helper to simulate new ow state output format using v1 state for development purposes.
    Previous state owbjects are created from known state map in OWdata and is not complete.
    """
    known_ow_state = OwDataV1(**known_ow_state_dict)

    ow_objects_state = OwData(ow_objects={}, terminated_ow_ids=[])

    # begin with existing OWObjects from known state OwData
    for ow_id, ow_tekstdeel_map in known_ow_state.object_map.tekstdeel_mapping.items():
        ow_obj = OWTekstdeel(OW_ID=ow_id, locaties=[ow_tekstdeel_map.location], divisie=ow_tekstdeel_map.divisie)
        ow_objects_state.ow_objects[ow_obj.OW_ID] = ow_obj

    for werkingsgebied_code, ow_id in known_ow_state.object_map.id_mapping.gebieden.items():
        ow_obj = OWGebied(OW_ID=ow_id, mapped_geo_code=werkingsgebied_code, mapped_uuid=None)
        ow_objects_state.ow_objects[ow_obj.OW_ID] = ow_obj

    for werkingsgebied_code, ow_id in known_ow_state.object_map.id_mapping.gebiedengroep.items():
        related_gebied_id = known_ow_state.object_map.id_mapping.gebieden[werkingsgebied_code]
        ow_obj = OWGebiedenGroep(
            OW_ID=ow_id,
            mapped_geo_code=werkingsgebied_code,
            mapped_uuid=None,
            gebieden=[related_gebied_id],
        )
        ow_objects_state.ow_objects[ow_obj.OW_ID] = ow_obj

    for uuid_str, ow_id in known_ow_state.object_map.id_mapping.ambtsgebied.items():
        bg = BestuurlijkeGrenzenVerwijzing(bestuurlijke_grenzen_id="", domein="", geldig_op="")
        ow_obj = OWAmbtsgebied(OW_ID=ow_id, mapped_uuid=UUID(uuid_str), bestuurlijke_grenzen_verwijzing=bg)
        ow_objects_state.ow_objects[ow_obj.OW_ID] = ow_obj

    for ambtsgebied_ow_id, ow_id in known_ow_state.object_map.id_mapping.regelingsgebied.items():
        ow_obj = OWRegelingsgebied(OW_ID=ow_id, ambtsgebied=ambtsgebied_ow_id)
        ow_objects_state.ow_objects[ow_obj.OW_ID] = ow_obj

    for wid, ow_id in known_ow_state.object_map.id_mapping.wid.items():
        ow_obj = OWDivisieTekst(OW_ID=ow_id, wid=wid)
        ow_objects_state.ow_objects[ow_obj.OW_ID] = ow_obj

    return ow_objects_state
