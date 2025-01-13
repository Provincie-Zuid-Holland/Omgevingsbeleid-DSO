from lxml import etree

from dso.act_builder.state_manager.state_manager import StateManager
from dso.act_builder.state_manager.states.text_manipulator.enricher.abstract_enricher import AbstractEnricher
from dso.act_builder.state_manager.states.text_manipulator.models import TekstPolicyObject, TextData


class ObjectIntrefEnricher(AbstractEnricher):
    def __init__(self, state_manager: StateManager):
        self._text_data: TextData = state_manager.text_data

    def enrich_xml(self, xml_content: str) -> str:
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(xml_content.encode("utf-8"), parser)

        for intref in root.xpath("//IntRef[@data-hint-target-object-code]"):
            object_code: str = intref.get("data-hint-target-object-code")
            text_policy_object: TekstPolicyObject = self._text_data.get_policy_object_by_code(object_code)

            intref.set("ref", text_policy_object.eid)
            intref.set("scope", text_policy_object.element)

        output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
        return output
