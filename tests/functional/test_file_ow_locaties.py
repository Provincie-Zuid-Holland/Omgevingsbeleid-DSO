
from pathlib import Path
from typing import List, Optional
import pytest
from lxml import etree

# These scenarios will run as input for every test case
TEST_SCENARIO_DIRS = [
    "./input/01-initial",
    "./input/02-mutation",
    "./input/03-add-gba",
]

@pytest.mark.parametrize("input_dir", TEST_SCENARIO_DIRS, indirect=True)
@pytest.mark.usefixtures("initialize_dso_builder")
class TestOWLocatiesFileOutput:
    output_dir: Optional[Path] = None

    @pytest.fixture(autouse=True)
    def check_locaties(self, expected_results):
        if "owLocaties" not in expected_results:
            pytest.skip("No owLocaties data in expected results")
        return expected_results["owLocaties"]

    def test_ow_locatie_count(self, expected_results, namespaces):
        expected_obj_count = expected_results["owLocaties"]["total"]
        tree = etree.parse(f"{self.output_dir}/owLocaties.xml", parser=None)
        root = tree.getroot()

        obj_count = len(root.findall(".//ow-dc:owObject", namespaces=namespaces))
        assert obj_count == expected_obj_count, f"Expected object count {expected_obj_count}, found {obj_count}"

    def test_new_ow_gebieden(self, expected_results, namespaces):
        expected_gebieden = expected_results["owLocaties"]["gebied"]["new"]

        # Parse the XML file
        tree = etree.parse(f"{self.output_dir}/owLocaties.xml", parser=None)
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
        """ensure any ambtsgebied changes reflect in both owlocaties and owregelingsgebied"""
        expected_ambtsgebied = expected_results["owLocaties"]["ambtsgebied"]

        tree = etree.parse(f"{self.output_dir}/owLocaties.xml", parser=None)
        root = tree.getroot()

        ambtsgebied = root.xpath(".//l:Ambtsgebied", namespaces=namespaces)

        if expected_ambtsgebied:
            assert len(ambtsgebied) == 1, f"Expected one Ambtsgebied, found {len(ambtsgebied)}"
        else:
            assert len(ambtsgebied) == 0, "Expected no Ambtsgebied, but found one"
