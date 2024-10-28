from pathlib import Path
from typing import List, Optional
import pytest
from lxml import etree

# These scenarios will run as input for every test case
TEST_SCENARIO_DIRS = [
    "./input/01-initial",
    "./input/02-mutation",
]

@pytest.mark.parametrize("input_dir", TEST_SCENARIO_DIRS, indirect=True)
@pytest.mark.usefixtures("initialize_dso_builder")
class TestPackageFileOutput:
    """
    Note:
    E2E tests over multiple mock scenario folders.
    uses the expected_results.yaml/json file for each scenario folder to
    validate the xml output.
    """
    output_dir: Optional[Path] = None

    def test_expected_files_exist(self, expected_results):
        """
        Ensure all expected files from package_files list are found in the output directory.
        """
        expected_files = expected_results["package_files"]
        assert self.output_dir is not None, "Output directory not set"
        for file in expected_files:
            assert (self.output_dir / file).exists(), f"Expected file {file} not found in output directory"

    def test_act_expected_wids_used(self, expected_results, namespaces):
        file_list = expected_results["package_files"]
        # find single file that starts with pattern akn_ and ends with .xml
        bill_file = next(file for file in file_list if file.startswith("akn_") and file.endswith(".xml"))

        tree = etree.parse(f"{self.output_dir}/{bill_file}", parser=None)
        root = tree.getroot()
        wids = expected_results["wids_used"]
        for wId in wids:
            assert root.xpath(
                f".//*[@wId='{wId}']", namespaces=namespaces
            ), f"Expected wId {wId} not found in {bill_file}"

    def test_manifest_content(self, expected_results, namespaces):
        expected_manifest = expected_results["package_files"]

        manifest_results = []
        tree = etree.parse(f"{self.output_dir}/manifest.xml", parser=None)
        root = tree.getroot()

        for bestand in root.findall(".//lvbb:bestand", namespaces=namespaces):
            bestandsnaam = bestand.find(".//lvbb:bestandsnaam", namespaces=namespaces)
            content_type = bestand.find(".//lvbb:contentType", namespaces=namespaces)
            manifest_results.append({"bestandsnaam": bestandsnaam.text, "content_type": content_type.text})

        # ensure every expected file is found in the manifest bestandsnaam
        for file in expected_manifest:
            assert any(
                file in result["bestandsnaam"] for result in manifest_results
            ), f"Expected file {file} not found in manifest"

    def test_ow_locatie_count(self, expected_results, namespaces):
        expected_obj_count = expected_results["owLocaties"]["total"]
        tree = etree.parse(f"{self.output_dir}/owLocaties.xml", parser=None)
        root = tree.getroot()

        obj_count = len(root.findall(".//ow-dc:owObject", namespaces=namespaces))
        assert obj_count == expected_obj_count, f"Expected object count {expected_obj_count}, found {obj_count}"

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
                f".//vt:Tekstdeel[vt:divisieaanduiding/vt:DivisietekstRef/@xlink:href='{div_id}']", namespaces=namespaces
            )
            assert tekstdeel, f"Expected a new Tekstdeel with DivisietekstRef {div_id}."
            # TODO: assert correct locationRef?


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

    def test_gml_file_ids(self, expected_results, namespaces):
        expected_geo_identifiers = expected_results["geo"]["identifiers"]
        geo_ids = set()
        gml_files = [file for file in expected_results["package_files"] if file.endswith(".gml")]
        for gml_file in gml_files:
            tree = etree.parse(f"{self.output_dir}/{gml_file}", parser=None)
            gml_root = tree.getroot()
            geometry = gml_root.xpath(".//basisgeo:Geometrie[basisgeo:id]", namespaces=namespaces)
            geo_ids.add(geometry[0][0].text)

        assert geo_ids == set(expected_geo_identifiers), "GML IDs do not match expected geo identifiers"

    def test_gio_uris(self, expected_results, namespaces):
        expected_gio_uris = expected_results["geo"]["uris"]

        gio_files = [
            file for file in expected_results["package_files"] if file.startswith("GIO_") and file.endswith(".xml")
        ]
        output_gio_uris = []
        for gio_file in gio_files:
            tree = etree.parse(f"{self.output_dir}/{gio_file}", parser=None)
            gio_root = tree.getroot()
            output_gio_uris.append(gio_root.find(".//data:FRBRExpression", namespaces=namespaces).text)

        # ensure for every expected gio uri, only 1 corresponding GIO file exists
        assert output_gio_uris == expected_gio_uris, "GIO URIs do not match expected URIs"

        bill_file = next(
            file for file in expected_results["package_files"] if file.startswith("akn_") and file.endswith(".xml")
        )

        tree = etree.parse(f"{self.output_dir}/{bill_file}", parser=None)
        root = tree.getroot()

        # check io refs in bill file
        informatieobject_refs = root.findall(
            ".//data:informatieobjectRefs/data:informatieobjectRef", namespaces=namespaces
        )
        for ref in informatieobject_refs:
            assert ref.text in expected_gio_uris, f"<informatieobjectRef> {ref.text} does not match expected GIO list"

        # check consolidatie informatie in bill file
        instrument_versies = root.findall(
            ".//data:ConsolidatieInformatie//data:instrumentVersie", namespaces=namespaces
        )
        consolidatie_instr_versies = [iv.text for iv in instrument_versies]

        for uri in expected_gio_uris:
            assert uri in consolidatie_instr_versies, f"Expected URI {uri} not found in <instrumentVersie> elements"

        # check tekst reference
        io_refs = root.findall(".//tekst:ExtIoRef", namespaces=namespaces)
        io_ref_attrs = [io_ref.get("ref") for io_ref in io_refs]
        for uri in expected_gio_uris:
            assert uri in io_ref_attrs, f"Expected URI {uri} not found in <ExtIoRef> attributes"
