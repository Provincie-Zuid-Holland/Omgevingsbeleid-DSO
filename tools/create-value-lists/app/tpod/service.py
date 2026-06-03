import io
import zipfile
from pathlib import Path

import requests

from ..util.ruff import format_with_ruff

from .config import DOWNLOAD_URL, SOURCE_FILE, TARGET_FILE, TARGET_PATH
from .processor_gebiedsaanwijzingen import GebiedsaanwijzingProcessor
from .processor_thema import ThemaProcessor
from .registry import WaardelijstProcessorRegistry
from .source_models import SourceResult


def do_create_waardelijsten():
    """
    This file has more "waardelijsten" than we need.
    We're processing only the ones we actually use.
    """

    registry: WaardelijstProcessorRegistry = WaardelijstProcessorRegistry()
    registry.add("gebiedsaanwijzingen", GebiedsaanwijzingProcessor())
    registry.add("themas", ThemaProcessor())

    print("Downloading source...")
    source: SourceResult = _download_source()
    for name, processor in registry.get_all().items():
        print(f"Processing {name}...")
        contents = processor.process(source)
        formatted_contents: str = format_with_ruff(contents)

        target_path = Path("../../") / TARGET_PATH.format(name=name) / TARGET_FILE
        resolved_path = target_path.resolve()

        with open(resolved_path, "w", encoding="utf-8") as f:
            f.write(formatted_contents)

        print(f"Processed {name}")


def _download_source() -> SourceResult:
    resp = requests.get(DOWNLOAD_URL)
    resp.raise_for_status()
    zip_bytes = io.BytesIO(resp.content)

    with zipfile.ZipFile(zip_bytes, "r") as z:
        with z.open(SOURCE_FILE) as f:
            return SourceResult.model_validate_json(f.read())
