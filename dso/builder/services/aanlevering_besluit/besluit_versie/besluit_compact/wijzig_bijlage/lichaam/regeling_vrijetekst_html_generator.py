from copy import copy

from lxml import etree
from lxml import html as lxml_html

from .......state_manager.input_data.object_template_repository import ObjectTemplateRepository
from .......state_manager.input_data.resource.policy_object.policy_object_repository import PolicyObjectRepository
from .......state_manager.state_manager import StateManager


class RegelingVrijetekstHtmlGenerator:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self):
        html: str = self._resolve_objects()

        return html

    # This parses the <object code="type-id" /> into the corresponding html for that object
    def _resolve_objects(self) -> str:
        policy_object_repository: PolicyObjectRepository = (
            self._state_manager.input_data.resources.policy_object_repository
        )
        object_template_repository: ObjectTemplateRepository = self._state_manager.input_data.object_template_repository
        html_str: str = self._state_manager.input_data.regeling_vrijetekst

        tree = lxml_html.fromstring(html_str)
        objects = tree.xpath("//object")

        for obj_xml in objects:
            attributes = copy(obj_xml.attrib)
            if "code" not in attributes:
                raise RuntimeError(f"Missing required attribute code for object")
            object_code: str = attributes["code"]
            
            if "template_name" in attributes:
                template_name = attributes["template_name"]
                object_template = object_template_repository.get_by_type(template_name)
            else:
                object_template = object_template_repository.get_by_code(object_code)

            policy_object = policy_object_repository.get_by_code(object_code)
            object_html: str = object_template.render(
                o=policy_object.data,
            )

            new_elements = lxml_html.fragments_fromstring(object_html)

            parent = obj_xml.getparent()
            for new_element in new_elements:
                parent.insert(parent.index(obj_xml), new_element)
            parent.remove(obj_xml)

        result = etree.tostring(tree, pretty_print=False).decode()
        return result
