import json
from pathlib import Path

import pytest


@pytest.fixture
def enable_debugpy():
    """Fixture to enable debugpy for debugging when needed."""
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger attach...")
    debugpy.wait_for_client()
    print("Debugger attached...")


@pytest.fixture(scope="session")
def input_data_werkingsgebieden():
    """Fixture to load werkingsgebied data from a JSON file."""
    json_file_path = Path(__file__).parent / "fixtures/werkingsgebied-example.json"
    with open(json_file_path, "r") as f:
        return json.load(f)
