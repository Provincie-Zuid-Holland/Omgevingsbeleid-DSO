from pathlib import Path
from typing import Optional


class XMLCompareTest:
    @staticmethod
    def _get_xml_file_path(current_path: str, idx: Optional[int] = None) -> str:
        test_file = Path(current_path).name
        base = test_file.removeprefix("test_").removesuffix(".py")

        if idx is not None:
            base = f"{base}_{idx}"

        xml_filename = f"{base}.xml"
        xml_path = Path(current_path).parent / xml_filename
        return xml_path
