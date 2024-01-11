# Change input URLS to needed waardelijst XMLs from STOP version.
# Generates python ENUMS to use e.g. in waardelijsten.py

import argparse
import re
import xml.etree.ElementTree as ET
from enum import Enum

import requests


def sanitize_key(key):
    key = key[0].upper() + key[1:]
    # Remove words in parenthesis
    key = re.sub(r"\([^)]*\)", "", key)
    # Remove spaces and non-allowed characters
    key = re.sub(r"\W+", "", key)
    return key


def generate_enum_from_url(url):
    namespaces = {"rsc": "https://standaarden.overheid.nl/stop/imop/resources/"}
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        enum_dict = {}
        for elem in root.findall(".//rsc:Waarde", namespaces):
            id_value = elem.find("rsc:id", namespaces).text
            label_value = elem.find("rsc:label", namespaces).text
            label_sanitized = sanitize_key(label_value)
            enum_dict[label_sanitized] = id_value

        class_name = root.find(".//rsc:label", namespaces=namespaces).text
        enum_type = Enum(sanitize_key(class_name), enum_dict)
        return enum_type
    else:
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Enum from XML URL")
    parser.add_argument("--url", required=True, help="URL to fetch the XML from")
    args = parser.parse_args()
    created_enum = generate_enum_from_url(args.url)
    if created_enum:
        print(f"#{str(args.url)}")
        class_definition = f"class {created_enum.__name__}(Enum):"
        print(class_definition)
        for name, member in created_enum.__members__.items():
            print(f'{name} = "{member.value}"')
    else:
        print("Failed to generate Enum. Check the URL or XML structure.")
