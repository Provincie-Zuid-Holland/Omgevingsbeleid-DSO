from pathlib import Path
from xml.etree import ElementTree


class XMLCompareTest:
    @staticmethod
    def _normalize_xml(xml: str) -> str:
        root = ElementTree.fromstring(xml)
        return ElementTree.tostring(root, encoding="unicode")

    @staticmethod
    def _get_xml_file_path(current_path: str) -> str:
        test_file = Path(current_path).name
        base = test_file.removeprefix("test_").removesuffix(".py")
        xml_filename = f"{base}.xml"
        xml_path = Path(current_path).parent / xml_filename
        return xml_path
