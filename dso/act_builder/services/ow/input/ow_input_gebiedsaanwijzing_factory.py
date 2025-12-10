from typing import List, Set

from dso.act_builder.services.ow.input.models import (
    OwInputAbstractLocatieRef,
    OwInputGebiedsaanwijzing,
    OwInputGebiedengroepLocatieRef,
)
from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.models import TekstPolicyObject, TextData


class OwInputGebiedsaanwijzingFactory:
    def __init__(self, state_manager: StateManager):
        self._werkingsgebieden_repository: WerkingsgebiedRepository = (
            state_manager.input_data.resources.werkingsgebied_repository
        )
        self._text_data: TextData = state_manager.text_data

    def get_gebiedsaanwijzingen(self) -> List[OwInputGebiedsaanwijzing]:
        result: Set[OwInputGebiedsaanwijzing] = set()

        for tekst_policy_object in self._text_data.policy_objects:
            object_aanwijzingen = self._build_for_policy_object(tekst_policy_object)
            result.update(object_aanwijzingen)

        return list(result)

    def _build_for_policy_object(self, tekst_policy_object: TekstPolicyObject) -> Set[OwInputGebiedsaanwijzing]:
        result: Set[OwInputGebiedsaanwijzing] = set()

        for tekst_gebiedsaanwijzingen in tekst_policy_object.gebiedsaanwijzingen:
            werkingsgebied: Werkingsgebied = self._werkingsgebieden_repository.get_by_code(
                tekst_gebiedsaanwijzingen.werkingsgebied_code
            )

            ow_input_gebiedsaanwijzingen = OwInputGebiedsaanwijzing(
                source_werkingsgebied_code=tekst_gebiedsaanwijzingen.werkingsgebied_code,
                title=werkingsgebied.Title,
                indication_type=tekst_gebiedsaanwijzingen.aanwijzing_type,
                indication_group=tekst_gebiedsaanwijzingen.aanwijzing_groep,
                location_refs=self._get_location_refs(werkingsgebied),
            )
            result.add(ow_input_gebiedsaanwijzingen)

        return result

    def _get_location_refs(self, werkingsgebied: Werkingsgebied) -> List[OwInputAbstractLocatieRef]:
        return [OwInputGebiedengroepLocatieRef(code=werkingsgebied.Code)]
