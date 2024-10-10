import hashlib
import json
import os
import zipfile
from io import StringIO
from xml.dom import minidom

import pkg_resources
from jinja2 import Environment, FileSystemLoader
from lxml import etree

from ...exceptions import FileWriteError, TemplateError
from .jinja_filters import jinja2_filter_has_text

# env = Environment(loader=FileSystemLoader("."))

template_path = pkg_resources.resource_filename("dso", "templates")

jinja2_env = Environment(
    loader=FileSystemLoader(template_path),
)
# Add the filters to the environment
jinja2_env.filters["has_text"] = jinja2_filter_has_text


def load_template(template_name: str, pretty_print: bool = False, **context) -> str:
    template = jinja2_env.get_template(f"/{template_name}")

    try:
        output = template.render(**context)
    except Exception as e:
        raise TemplateError(template_name, f"Error rendering template: {str(e)}")

    if pretty_print:
        try:
            if output.startswith("<?xml"):
                parser = etree.XMLParser(remove_blank_text=True)
                tree = etree.fromstring(output.encode("utf-8"), parser=parser)
            else:
                tree = etree.fromstring(output)
            output = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8")
        except Exception as e:
            raise TemplateError(template_name, f"Error pretty printing: {str(e)}")

    return output


def load_template_and_write_file(template_name, output_file, pretty_print=False, **context):
    output = load_template(template_name, pretty_print=pretty_print, **context)
    try:
        with open(output_file, "w") as f:
            f.write(output)
    except Exception as e:
        raise FileWriteError(output_file, str(e))


def write_file(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)


def get_file_entries(folder_path, content_type_map):
    file_entries = []
    for filename in os.listdir(folder_path):
        extension = filename.split(".")[-1]
        content_type = content_type_map.get(extension)
        file_entries.append({"filename": filename, "contentType": content_type})
    return file_entries


def load_json_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def load_xml_file(file_path) -> str:
    with open(file_path, "r") as f:
        xml_content = f.read()

        return xml_content


def pretty_print_template_xml(content, output_file):
    # Wrap the content in a root element to allow parsing
    wrapped_content = f"<root>{content}</root>"
    dom = minidom.parseString(wrapped_content)
    pretty_xml = dom.toprettyxml(indent="   ")
    # Remove the root element tag added in wrapper
    pretty_xml = pretty_xml.replace("\n<root>\n", "").replace("\n</root>\n", "")

    pretty_lines = pretty_xml.split("\n")
    result_lines = [line for line in pretty_lines[1:-1] if line.strip()]
    result = "\n".join(result_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)


# def load_werkingsgebieden(path="./input/werkingsgebieden/*.json") -> List[Werkingsgebied]:
#     return [Werkingsgebied(**load_json_data(wg_json)) for wg_json in glob.glob(path)]


def create_zip_from_dir(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)


def get_checksum_and_size(file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_size = len(file_content)
    checksum = hashlib.sha256(file_content).hexdigest()
    return checksum, file_size


def is_html_valid(html_content) -> bool:
    try:
        parser = etree.HTMLParser(recover=False)
        etree.parse(StringIO(html_content), parser)
        return True
    except etree.XMLSyntaxError:
        return False


def to_lowercase_keys(data):
    if isinstance(data, dict):
        return {k.lower(): to_lowercase_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [to_lowercase_keys(i) for i in data]
    else:
        return data
