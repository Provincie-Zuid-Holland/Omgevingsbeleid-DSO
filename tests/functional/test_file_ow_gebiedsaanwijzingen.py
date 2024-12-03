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
class TestOWGebiedsaanwijzingenFileOutput:
    output_dir: Optional[Path] = None

    @pytest.fixture(autouse=True)
    def check_gebiedsaanwijzingen(self, expected_results):
        if "owGebiedsaanwijzingen" not in expected_results:
            pytest.skip("No owGebiedsaanwijzingen data in expected results")
        return expected_results["owGebiedsaanwijzingen"]

    def test_ow_gebiedsaanwijzing_count(self, expected_results, namespaces):
        expected_obj_count = expected_results["owGebiedsaanwijzingen"]["total"]
        tree = etree.parse(f"{self.output_dir}/owGebiedsaanwijzingen.xml", parser=None)
        root = tree.getroot()

        obj_count = len(root.findall(".//ow-dc:owObject", namespaces=namespaces))
        assert obj_count == expected_obj_count, f"Expected object count {expected_obj_count}, found {obj_count}"

    def test_new_ow_gebiedsaanwijzing_content(self, expected_results, namespaces):
        expected_obj_list = expected_results["owGebiedsaanwijzingen"]["gebiedsaanwijzing"]["new"]
        tree = etree.parse(f"{self.output_dir}/owGebiedsaanwijzingen.xml", parser=None)
        root = tree.getroot()

        for expected_obj in expected_obj_list:
            gba = root.find(f".//ga:Gebiedsaanwijzing[ga:naam='{expected_obj['noemer']}']", namespaces=namespaces)
            status = gba.find("ow:status", namespaces=namespaces)
            assert status is None, f"Found unexpected status tag in object {expected_obj['noemer']}"
            assert gba is not None, f"Expected object {expected_obj} not found"
            assert gba.find("ga:type", namespaces=namespaces).text == expected_obj["type_"], \
                f"Expected type {expected_obj['type_']}, found {gba.find('ga:type', namespaces=namespaces).text}"
            assert gba.find("ga:groep", namespaces=namespaces).text == expected_obj["groep"], \
                f"Expected groep {expected_obj['groep']}, found {gba.find('ga:groep', namespaces=namespaces).text}"


    def test_mutated_ow_gebiedsaanwijzing_content(self, expected_results, namespaces):
        expected_obj_list = expected_results["owGebiedsaanwijzingen"]["gebiedsaanwijzing"]["mutated"]
        tree = etree.parse(f"{self.output_dir}/owGebiedsaanwijzingen.xml", parser=None)
        root = tree.getroot()

        for expected_obj in expected_obj_list:
            gba = root.find(f".//ga:Gebiedsaanwijzing[ga:naam='{expected_obj['noemer']}']", namespaces=namespaces)
            status = gba.find("ow:status", namespaces=namespaces)
            assert status is None, f"Found unexpected status tag in object {expected_obj['noemer']}"
            assert gba is not None, f"Expected object {expected_obj} not found"
            assert gba.find("ga:type", namespaces=namespaces).text == expected_obj["type_"], \
                f"Expected type {expected_obj['type_']}, found {gba.find('ga:type', namespaces=namespaces).text}"
            assert gba.find("ga:groep", namespaces=namespaces).text == expected_obj["groep"], \
                f"Expected groep {expected_obj['groep']}, found {gba.find('ga:groep', namespaces=namespaces).text}"

    def test_terminated_ow_gebiedsaanwijzing_content(self, expected_results, namespaces):
        expected_obj_list = expected_results["owGebiedsaanwijzingen"]["gebiedsaanwijzing"]["terminated"]
        tree = etree.parse(f"{self.output_dir}/owGebiedsaanwijzingen.xml", parser=None)
        root = tree.getroot()

        for expected_obj in expected_obj_list:
            gba = root.find(f".//ga:Gebiedsaanwijzing[ga:naam='{expected_obj['noemer']}']", namespaces=namespaces)
            status = gba.find("ow:status", namespaces=namespaces)
            assert status is not None, f"Expected status tag in object {expected_obj['noemer']}"
            assert gba is not None, f"Expected object {expected_obj} not found"
            assert gba.find("ga:type", namespaces=namespaces).text == expected_obj["type_"], \
                f"Expected type {expected_obj['type_']}, found {gba.find('ga:type', namespaces=namespaces).text}"
            assert gba.find("ga:groep", namespaces=namespaces).text == expected_obj["groep"], \
                f"Expected groep {expected_obj['groep']}, found {gba.find('ga:groep', namespaces=namespaces).text}"