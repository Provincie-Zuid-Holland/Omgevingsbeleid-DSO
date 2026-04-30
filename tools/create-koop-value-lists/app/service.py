import io
import re
import subprocess
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict

import requests

from config import (
    DOWNLOAD_URL,
    SOURCE_FOLDER,
    VERSION,
    DOWNLOAD_FILE,
    TARGET_FILE,
    IGNORE_FILES,
    XML_NAMESPACES,
)

OUTPUT_FILE_HEADING = """
# GENERATED FILE - DO NOT EDIT

from enum import Enum
"""


def _sanitize_key(key: str) -> str:
    key = key[0].upper() + key[1:]
    # Remove words in parentheses
    key = re.sub(r"\([^)]*\)", "", key)
    # Remove spaces and non-allowed characters
    key = re.sub(r"\W+", "", key)
    return key


def _get_text_value_for_element(xml_element: ET.Element, path: str, default_value: str = "") -> str:
    the_element: Optional[ET.Element] = xml_element.find(path, XML_NAMESPACES)
    if the_element is None:
        raise RuntimeWarning(f"Can't find XML element using path '{path}'")
    value: str = the_element.text or default_value
    return value


def _remove_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _download_source() -> List[Enum]:
    download_url = DOWNLOAD_URL.replace("[version]", VERSION)
    download_file = DOWNLOAD_FILE.replace("[version]", VERSION)
    zip_folder = download_file.removesuffix(".zip")

    resp = requests.get(f"{download_url}/{download_file}")
    resp.raise_for_status()
    zip_bytes = io.BytesIO(resp.content)

    enums: List[Enum] = []

    with zipfile.ZipFile(zip_bytes, "r") as z:
        xml_files = [
            name
            for name in z.namelist()
            if name.startswith(f"{zip_folder}/{SOURCE_FOLDER}")
            and name.endswith(".xml")
            and not any(name.endswith(f"{ignore_file}.xml") for ignore_file in IGNORE_FILES)
        ]

        for file_name in xml_files:
            with z.open(file_name) as f:
                root: ET.Element[str] = ET.fromstring(f.read())
                enum_dict: Dict[str, str] = {}
                for element in root.findall(".//rsc:Waarde", XML_NAMESPACES):
                    id_value = _get_text_value_for_element(element, "rsc:id")
                    label_value = _get_text_value_for_element(element, "rsc:label")
                    label_sanitized = _remove_accents(_to_camel_case(label_value))
                    enum_dict[label_sanitized] = id_value

                if len(enum_dict.keys()) <= 0:
                    continue

                class_name: str = _get_text_value_for_element(root, ".//rsc:label")
                class_name_camel_case: str = _to_camel_case(class_name)
                enum_type: Enum = Enum(class_name_camel_case, enum_dict)
                enums.append(enum_type)
    return enums


def _format_with_ruff(code: str) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path: Path = Path(tmp.name)

    subprocess.run(["ruff", "check", "--fix", str(tmp_path)], check=True)
    subprocess.run(["ruff", "format", str(tmp_path)], check=True)

    formatted: str = tmp_path.read_text()
    tmp_path.unlink()

    return formatted


def _to_camel_case(input: str) -> str:
    parts = re.split(r"[_\-\s()'.,]+", input)
    parts = [p for p in parts if p]  # remove empty chunks
    return "".join(word.capitalize() for word in parts)


def do_create_waardelijsten():
    output_contents: List[str] = []
    output_contents.append(OUTPUT_FILE_HEADING)

    enums = _download_source()
    for enum in enums:
        output_contents.append(f"class {enum.__name__}(str, Enum):")
        for member in enum:
            output_contents.append(f"\t{member.name} = {repr(member.value)}")

    final_output_contents: str = "\n".join(output_contents)
    target_path = Path(".") / TARGET_FILE
    resolved_path = target_path.resolve()

    formatted_contents: str = _format_with_ruff(final_output_contents)

    with open(resolved_path, "w", encoding="utf-8") as f:
        f.write(formatted_contents)

    print("Done!")
