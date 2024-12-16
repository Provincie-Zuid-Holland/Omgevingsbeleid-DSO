from pathlib import Path
from typing import List, Optional
import pytest
from lxml import etree

# These scenarios will run as input for every test case
TEST_SCENARIO_DIRS = ["./input/01-initial", "./input/02-mutation", "./input/03-add-gba"]


@pytest.mark.parametrize("input_dir", TEST_SCENARIO_DIRS, indirect=True)
@pytest.mark.usefixtures("initialize_dso_builder")
class TestOWDivisiesFileOutput:
    output_dir: Optional[Path] = None

    @pytest.fixture(autouse=True)
    def check_divisies(self, expected_results):
        if "owDivisies" not in expected_results:
            pytest.skip("No owDivisies data in expected results")
        return expected_results["owDivisies"]

    def test_ow_divisie_count(self, expected_results, namespaces):
        expected_obj_count = expected_results["owDivisies"]["total"]
        tree = etree.parse(f"{self.output_dir}/owDivisies.xml", parser=None)
        root = tree.getroot()

        obj_count = len(root.findall(".//ow-dc:owObject", namespaces=namespaces))
        assert obj_count == expected_obj_count, f"Expected object count {expected_obj_count}, found {obj_count}"

    def test_new_ow_divisiestekst_objects(self, expected_results, namespaces):
        expected_div_wids: List[str] = expected_results["owDivisies"]["divisietekst"]["new"]
        tree = etree.parse(f"{self.output_dir}/owDivisies.xml", parser=None)
        root = tree.getroot()

        ow_divisie_elements = root.findall(".//vt:Divisietekst", namespaces=namespaces)

        ow_divisie_wids = []
        ow_divisie_ids = []
        for div in ow_divisie_elements:
            ow_divisie_wids.append(div.get("wId"))
            ow_divisie_ids.append(div.find(".//vt:identificatie", namespaces=namespaces).text)

        for div_id in ow_divisie_ids:
            tekstdeel = root.xpath(
                f".//vt:Tekstdeel[vt:divisieaanduiding/vt:DivisietekstRef/@xlink:href='{div_id}']",
                namespaces=namespaces,
            )
            assert tekstdeel, f"Expected a new Tekstdeel with DivisietekstRef {div_id}."
            # TODO: assert correct locationRef?
