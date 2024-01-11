from typing import Dict, List, Union

from jinja2 import Template


class ObjectTemplateRepository:
    def __init__(self, template_data: Dict[str, Union[str, List[str]]]):
        self._template_data: Dict[str, Template] = self._resolve_template_data(template_data)

    def get_by_code(self, object_code: str) -> Template:
        object_type, _ = object_code.split("-")
        return self.get_by_type(object_type)

    def get_by_type(self, object_type: str) -> Template:
        return self._template_data[object_type]

    def _resolve_template_data(self, template_data: Dict[str, Union[str, List[str]]]) -> Dict[str, Template]:
        result: Dict[str, Template] = {}

        for object_code, data in template_data.items():
            if isinstance(data, list):
                data = "".join(data)

            template = Template(data)
            result[object_code] = template

        return result
