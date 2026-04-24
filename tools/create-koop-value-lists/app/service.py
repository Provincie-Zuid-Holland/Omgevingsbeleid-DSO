import io
import re
import zipfile
from enum import Enum
from typing import List

import requests
import xml.etree.ElementTree as ET
from config import (
    DOWNLOAD_URL,
    SOURCE_FOLDER, VERSION, DOWNLOAD_FILE,
)
from source_models import SourceResult

OUTPUT_FILE_HEADING = """
# GENERATED FILE - DO NOT EDIT
""" # TODO add imports

def _sanitize_key(key: str) -> str:
    key = key[0].upper() + key[1:]
    # Remove words in parentheses
    key = re.sub(r"\([^)]*\)", "", key)
    # Remove spaces and non-allowed characters
    key = re.sub(r"\W+", "", key)
    return key


def _download_source() -> SourceResult:
    download_url = DOWNLOAD_URL.replace("[version]", VERSION)
    download_file = DOWNLOAD_FILE.replace("[version]", VERSION)
    zip_folder = download_file.removesuffix(".zip")

    namespaces = {"rsc": "https://standaarden.overheid.nl/stop/imop/resources/"} # TODO to config??

    resp = requests.get(f"{download_url}/{download_file}")
    resp.raise_for_status()
    zip_bytes = io.BytesIO(resp.content)

    enums: List[Enum] = []

    with zipfile.ZipFile(zip_bytes, "r") as z:
        xml_files = [name for name in z.namelist() if name.startswith(f"{zip_folder}/{SOURCE_FOLDER}") and name.endswith(".xml")]
        for file_name in xml_files:
            with z.open(file_name) as f:
                root = ET.fromstring(f.read())
                enum_dict = {}
                for elem in root.findall(".//rsc:Waarde", namespaces):
                    id_value = elem.find("rsc:id", namespaces).text
                    label_value = elem.find("rsc:label", namespaces).text
                    label_sanitized = _sanitize_key(label_value)
                    enum_dict[label_sanitized] = id_value
                class_name = root.find(".//rsc:label", namespaces=namespaces).text
                enum_type = Enum(_sanitize_key(class_name), enum_dict)
                enums.append(enum_type)

    return SourceResult()


def do_create_waardelijsten():
    source = _download_source()
    print(source)
