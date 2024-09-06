from typing import Dict, List, Set

from dso.act_builder.services.ow.ow_regelinggebied import OWRegelingsgebied

from ...act_builder.state_manager.exceptions import OWStateDanglingObjectsException
from ...act_builder.state_manager.states.ow_repository import OwData
from .models import OWGebiedenGroep, OWObject, OWTekstdeel


# TODO: remove as is kept in ow state patcher now instead
class OWStateValidator:
    def __init__(self, ow_data: OwData):
        self._ow_data = ow_data.copy(deep=True)
        self._valid: bool = False
        self._reverse_ref_index: Dict[str, Set[str]] = {}
        self._dangling_objects: List["OWObject"] = []

    def preprocess_state(self, ow_objects_map: Dict[str, "OWObject"]) -> Dict[str, Set[str]]:
        self._reverse_ref_index = {
            "OWTekstdeel": set(),
            "OWGebiedenGroep": set(),
            "OWRegelingsgebied": set(),
        }

        for ow_obj in ow_objects_map.values():
            if isinstance(ow_obj, OWTekstdeel):
                for locatie_id in ow_obj.locaties:
                    self._reverse_ref_index["OWTekstdeel"].add(locatie_id)
                self._reverse_ref_index["OWTekstdeel"].add(ow_obj.divisie)
            if isinstance(ow_obj, OWGebiedenGroep):
                for gebied_id in ow_obj.gebieden:
                    self._reverse_ref_index["OWGebiedenGroep"].add(gebied_id)
            if isinstance(ow_obj, OWRegelingsgebied):
                self._reverse_ref_index["OWRegelingsgebied"].add(ow_obj.ambtsgebied)

        return self._reverse_ref_index

    def find_dangling_objects(self) -> List["OWObject"]:
        """Check for OWObjects that are not referenced by any other objects."""
        self._dangling_objects: List["OWObject"] = []  # Use the class attribute
        reverse_index = self.preprocess_state(self._ow_data.ow_objects)

        # Collect IDs from all relationships
        for ow_obj in self._ow_data.ow_objects.values():
            if not ow_obj.has_valid_refs(self._ow_data.used_ow_ids, reverse_index):
                self._dangling_objects.append(ow_obj)

        return self._dangling_objects

    def _validate_no_dangling_objects(self) -> bool:
        dangling_objects = self.find_dangling_objects()
        if dangling_objects:
            raise OWStateDanglingObjectsException(
                message=f"Found dangling OWObjects: {[obj.OW_ID for obj in dangling_objects]}",
                ow_objects=dangling_objects,
            )
        return True

    def validate(self) -> None:
        """Run all required state validation checks."""
        self._validate_no_dangling_objects()
        self._valid = True
