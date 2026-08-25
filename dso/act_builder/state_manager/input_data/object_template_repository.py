from jinja2 import Template

from ....services.utils.helpers import jinja2_env


class ObjectTemplateRepository:
    def __init__(self, template_data: dict[str, str | list[str]]):
        self._template_source: dict[str, str | list[str]] = template_data
        self._template_data: dict[str, Template] = self._resolve_template_data(template_data)

    def get_by_code(self, object_code: str) -> Template:
        object_type, _ = object_code.split("-")
        return self.get_by_type(object_type)

    def get_by_type(self, object_type: str) -> Template:
        return self._template_data[object_type]

    def _resolve_template_data(self, template_data: dict[str, str | list[str]]) -> dict[str, Template]:
        result: dict[str, Template] = {}

        for object_code, data in template_data.items():
            if isinstance(data, list):
                data = "".join(data)

            template = jinja2_env.from_string(data)
            result[object_code] = template

        return result

    def get_source_data(self) -> dict[str, str | list[str]]:
        return self._template_source

    def to_dict(self):
        return self.get_source_data()
