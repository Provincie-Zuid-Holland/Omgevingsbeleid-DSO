import pytest
import json
from lxml import etree
from collections import defaultdict

from dso.services.ow.models import OWGebiedenGroep, OWGebied, OWDivisieTekst, OWDivisie

from .base import BaseTestBuilder


@pytest.fixture(scope="class")
def input_dir(request):
    return request.param


@pytest.fixture(scope="class")
def expected_results(input_dir):
    with open(f"{input_dir}/expected_results.json") as f:
        return json.load(f)


@pytest.fixture(scope="class")
def namespaces():
    namespaces = {
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xlink": "http://www.w3.org/1999/xlink",
        "r": "http://www.geostandaarden.nl/imow/regels",
        "vt": "http://www.geostandaarden.nl/imow/vrijetekst",
        "rol": "http://www.geostandaarden.nl/imow/regelsoplocatie",
        "p": "http://www.geostandaarden.nl/imow/pons",
        "l": "http://www.geostandaarden.nl/imow/locatie",
        "k": "http://www.geostandaarden.nl/imow/kaart",
        "op": "http://www.geostandaarden.nl/imow/opobject",
        "ga": "http://www.geostandaarden.nl/imow/gebiedsaanwijzing",
        "sl": "http://www.geostandaarden.nl/bestanden-ow/standlevering-generiek",
        "da": "http://www.geostandaarden.nl/imow/datatypenalgemeen",
        "ow": "http://www.geostandaarden.nl/imow/owobject",
        "rg": "http://www.geostandaarden.nl/imow/regelingsgebied",
        "ow-dc": "http://www.geostandaarden.nl/imow/bestanden/deelbestand",
    }
    return namespaces


@pytest.mark.parametrize(
    "input_dir",
    [
        "tests/functional/scenarios/01-initial",
    ],
    indirect=True,
)
class TestPackageOutputFiles(BaseTestBuilder):
    def test_expected_files_exist(self, expected_results):
        expected_files = expected_results["package_files"]
        assert self.output_dir is not None, "Output directory not set"
        # Add logic to check if the expected files exist in the output directory
        for file in expected_files:
            assert (self.output_dir / file).exists(), f"Expected file {file} not found in output directory"
        assert True

    def test_ow_gebieden(self, expected_results, namespaces):
        expected_gebieden = expected_results["owLocaties"]["gebieden"]

        # Parse the XML file
        tree = etree.parse(f"{self.output_dir}/owLocaties.xml")
        root = tree.getroot()

        for expected_gebied in expected_gebieden:
            noemer = expected_gebied["noemer"]
            geometrie_href = expected_gebied["geometrie_href"]

            # Find the Gebied element with the expected noemer
            gebied = root.xpath(f".//l:Gebied[l:noemer='{noemer}']", namespaces=namespaces)
            assert len(gebied) == 1, f"Expected one Gebied with noemer '{noemer}', found {len(gebied)}"
            gebied = gebied[0]

            # Check the GeometrieRef href
            geometrie_ref = gebied.find(".//l:GeometrieRef", namespaces=namespaces)
            assert (
                geometrie_ref.get("{http://www.w3.org/1999/xlink}href") == geometrie_href
            ), f"GeometrieRef href does not match for Gebied '{noemer}'"

            # Find the corresponding Gebiedengroep
            gebiedengroep = root.xpath(f".//l:Gebiedengroep[l:noemer='{noemer}']", namespaces=namespaces)
            assert (
                len(gebiedengroep) == 1
            ), f"Expected one Gebiedengroep with noemer '{noemer}', found {len(gebiedengroep)}"
            gebiedengroep = gebiedengroep[0]

            # Check the GebiedRef href matches the identificatie of the Gebied
            gebied_ref = gebiedengroep.find(".//l:GebiedRef", namespaces=namespaces)
            assert (
                gebied_ref.get("{http://www.w3.org/1999/xlink}href")
                == gebied.find(".//l:identificatie", namespaces=namespaces).text
            ), f"GebiedRef href does not match for Gebiedengroep '{noemer}'"

    def test_ow_ambtsgebied(self, expected_results, namespaces):
        expected_ambtsgebied = expected_results["owLocaties"]["ambtsgebied"]

        # Parse the XML file
        tree = etree.parse(f"{self.output_dir}/owLocaties.xml")
        root = tree.getroot()

        if expected_ambtsgebied:
            ambtsgebied = root.xpath(".//l:Ambtsgebied", namespaces=namespaces)
            assert len(ambtsgebied) == 1, f"Expected one Ambtsgebied, found {len(ambtsgebied)}"
            ambtsgebied = ambtsgebied[0]
