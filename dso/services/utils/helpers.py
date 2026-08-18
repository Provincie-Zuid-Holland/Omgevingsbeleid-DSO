import importlib.resources
import json
from io import StringIO
from typing import Any

from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateError as Jinja2TemplateError
from lxml import etree
from lxml.etree import XMLSyntaxError

from ...exceptions import TemplateError
from .jinja_filters import jinja2_filter_has_text

template_path = importlib.resources.files("dso") / "templates"

jinja2_env = Environment(
    loader=FileSystemLoader(template_path),
)
jinja2_env.filters["has_text"] = jinja2_filter_has_text


def load_template(template_name: str, pretty_print: bool = False, **context: Any) -> str:
    template = jinja2_env.get_template(f"/{template_name}")

    try:
        output = template.render(**context)
    except Jinja2TemplateError as e:
        raise TemplateError(template_name, f"Error rendering template: {e!s}") from e

    if pretty_print:
        try:
            if output.startswith("<?xml"):
                parser = etree.XMLParser(remove_blank_text=False)
                tree = etree.fromstring(output.encode("utf-8"), parser=parser)
            else:
                tree = etree.fromstring(output)
            output = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8")
        except XMLSyntaxError as e:
            raise TemplateError(template_name, f"Error pretty printing: {e!s}") from e

    return output


def load_json_data(file_path: str) -> dict | list:
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def load_xml_file(file_path: str) -> str:
    with open(file_path, encoding="utf-8") as f:
        xml_content = f.read()
        return xml_content


def is_html_valid(html_content: str) -> bool:
    try:
        parser = etree.HTMLParser(recover=False)
        etree.parse(StringIO(html_content), parser)
        return True
    except etree.XMLSyntaxError:
        return False


def to_lowercase_keys(data: Any) -> Any:
    if isinstance(data, dict):
        return {k.lower(): to_lowercase_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_lowercase_keys(i) for i in data]
    else:
        return data
