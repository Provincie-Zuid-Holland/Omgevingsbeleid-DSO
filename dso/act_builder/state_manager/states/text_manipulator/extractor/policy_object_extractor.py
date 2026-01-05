from typing import List

from lxml import etree

from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.models import (
    TekstPolicyObject,
    TekstPolicyObjectGebiedsaanwijzing,
)


class TextPolicyObjectExtractor:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def extract(self, xml_content: str):
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)
        elements = root.xpath("//*[@data-hint-object-code]")

        for element in elements:
            code: str = element.get("data-hint-object-code")
            eid: str = element.get("eId")
            wid: str = element.get("wId")

            gebiedsaanwijzingen: List[TekstPolicyObjectGebiedsaanwijzing] = self._extract_gebiedsaanwijzingen(element)

            self._state_manager.text_data.policy_objects.append(
                TekstPolicyObject(
                    object_code=code,
                    eid=eid,
                    wid=wid,
                    element=element.tag,
                    gebiedsaanwijzingen=gebiedsaanwijzingen,
                )
            )

    def _extract_gebiedsaanwijzingen(self, root) -> List[TekstPolicyObjectGebiedsaanwijzing]:
        result: List[TekstPolicyObjectGebiedsaanwijzing] = []

        elements = root.xpath("//*[@data-hint-type='gebiedsaanwijzing']")
        for element in elements:
            result.append(
                TekstPolicyObjectGebiedsaanwijzing(
                    uuid=element.get("data-hint-gebiedsaanwijzing-uuid"),
                    eid=element.get("eId"),
                    wid=element.get("wId"),
                    element=element.tag,
                )
            )
        return result
