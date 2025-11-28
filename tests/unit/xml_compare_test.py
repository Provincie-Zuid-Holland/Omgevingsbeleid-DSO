from pathlib import Path


class XMLCompareTest:
    @staticmethod
    def _get_xml_file_path(current_path: str) -> str:
        test_file = Path(current_path).name
        base = test_file.removeprefix("test_").removesuffix(".py")
        xml_filename = f"{base}.xml"
        xml_path = Path(current_path).parent / xml_filename
        return xml_path
