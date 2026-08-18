# ruff: noqa: T100
import json
import os
import shutil
from pathlib import Path

import pytest
import yaml

from dso.act_builder.builder import Builder
from dso.act_builder.state_manager.input_data.input_data_loader import InputData
from dso.cmds import build_input_data_from_dir
from tests.unit.dso.act_builder.state_manager.input_data.resource.document.document_repository import (
    document_repository_mock_with_two_documents,
    document_repository_mock_with_two_new_documents,
)  # noqa: F401
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import (
    gio_repository_mock_empty,
    gio_repository_mock_with_two_gebieden,
    gio_repository_mock_with_two_new_gebieden,
)  # noqa: F401  # noqa: F401  # noqa: F401
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import state_manager_mock  # noqa: F401
from tests.unit.dso.act_builder.state_manager.states.artikel_eid_repository import (
    artikel_eid_repository_with_eid_data,
)  # noqa: F401


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


@pytest.fixture(scope="class")
def input_dir(request):
    return request.param


@pytest.fixture(scope="class")
def output_dir(request, input_dir) -> Path:
    relative_path = str(Path(input_dir).relative_to(Path(input_dir).parents[0]))
    output_dir = Path("./output") / relative_path
    # Set output_dir as an attribute on the test class
    request.cls.output_dir = output_dir
    return output_dir


@pytest.fixture(scope="class")
def expected_results(input_dir):
    with open(f"{input_dir}/expected_results.yml") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="class")
def initialize_dso_builder(request, input_dir, output_dir) -> Builder:
    if input_dir is None:
        pytest.fail("No input scenario dir was provided")

    scenario_path = os.path.abspath(input_dir)

    if not os.path.isdir(scenario_path):
        pytest.fail(f"Test directory does not exist: {scenario_path}")

    # Setup Builder with the specified input directory
    input_data: InputData = build_input_data_from_dir(str(scenario_path))
    dso_builder = Builder(input_data)

    # Setup results for testing
    dso_builder.build_publication_files()

    if output_dir.exists() and output_dir.is_dir():
        shutil.rmtree(output_dir)  # remove existing

    dso_builder.save_files(str(output_dir))
    # Set dso_builder as an attribute on the test class if needed
    request.cls.dso_builder = dso_builder
    request.cls.state_manager = dso_builder._state_manager
    return dso_builder


@pytest.fixture(scope="class")
def namespaces():
    namespaces = {
        "basisgeo": "http://www.geostandaarden.nl/basisgeometrie/1.0",
        "da": "http://www.geostandaarden.nl/imow/datatypenalgemeen",
        "data": "https://standaarden.overheid.nl/stop/imop/data/",
        "ga": "http://www.geostandaarden.nl/imow/gebiedsaanwijzing",
        "geo": "https://standaarden.overheid.nl/stop/imop/geo/",
        "gio": "https://standaarden.overheid.nl/stop/imop/gio/",
        "gml": "http://www.opengis.net/gml/3.2",
        "k": "http://www.geostandaarden.nl/imow/kaart",
        "l": "http://www.geostandaarden.nl/imow/locatie",
        "lvbb": "http://www.overheid.nl/2017/lvbb",
        "op": "http://www.geostandaarden.nl/imow/opobject",
        "ow": "http://www.geostandaarden.nl/imow/owobject",
        "ow-dc": "http://www.geostandaarden.nl/imow/bestanden/deelbestand",
        "p": "http://www.geostandaarden.nl/imow/pons",
        "r": "http://www.geostandaarden.nl/imow/regels",
        "rg": "http://www.geostandaarden.nl/imow/regelingsgebied",
        "rol": "http://www.geostandaarden.nl/imow/regelsoplocatie",
        "sl": "http://www.geostandaarden.nl/bestanden-ow/standlevering-generiek",
        "tekst": "https://standaarden.overheid.nl/stop/imop/tekst/",
        "vt": "http://www.geostandaarden.nl/imow/vrijetekst",
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    return namespaces
