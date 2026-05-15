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

from koop.config import (
    DOWNLOAD_URL,
    SOURCE_FOLDER,
    VERSION,
    DOWNLOAD_FILE,
    TARGET_FILE,
    IGNORE_FILES,
    XML_NAMESPACES,
    NAME_MAPPING, MERGE_TYPES,
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

    print(f"Downloading {download_file}...")
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
                    label_value_snake_case = _to_snake_case(label_value)
                    label_sanitized = _remove_accents(label_value_snake_case)
                    enum_dict[label_sanitized] = id_value

                if len(enum_dict.keys()) <= 0:
                    continue

                class_name: str = _get_text_value_for_element(root, ".//rsc:label")
                class_name_mapped = NAME_MAPPING.get(class_name)
                if class_name_mapped is None:
                    raise RuntimeWarning(f"Can't find mapped class name for '{class_name}'")
                enum_type: Enum = Enum(class_name_mapped, enum_dict)
                enums.append(enum_type)

        for merge_type in MERGE_TYPES:
            merged_enum_dict: Dict[str, str] = {}
            for enum in enums:
                if enum.__name__ not in merge_type.koop_types:
                    continue
                for enum_member in enum.__members__:
                    merged_enum_dict[enum_member] = enum[enum_member].value

            merged_enum_type: Enum = Enum(merge_type.name, merged_enum_dict)
            enums.append(merged_enum_type)
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


def _get_parts(value: str) -> List[str]:
    parts = re.split(r"[_\-\s()'.,]+", value)
    parts = [p for p in parts if p]  # remove empty chunks
    return parts


def _to_snake_case(value: str) -> str:
    parts = _get_parts(value)
    return "_".join(word.lower() for word in parts)


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
