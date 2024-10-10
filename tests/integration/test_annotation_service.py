import json
import pytest

from lxml import etree
from pathlib import Path

from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from dso.services.ow.ow_annotation_service import OWAnnotationService


class TestOWAnnotationService:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize common resources."""
        # debugpy.listen(("0.0.0.0", 5678))
        # print("Waiting for debugger attach...")
        # debugpy.wait_for_client()
        # print("Debugger attached...")

        # Load Werkingsgebied data from a JSON file and populate the repository
        json_file_path = Path(__file__).parent.parent / "fixtures/werkingsgebied-example.json"
        with open(json_file_path, "r") as f:
            werkingsgebied_data = json.load(f)

        self.werkingsgebied_repository = WerkingsgebiedRepository()
        self.werkingsgebied_repository.add_from_dict(werkingsgebied_data)

        self.annotation_service = OWAnnotationService(
            werkingsgebied_repository=self.werkingsgebied_repository,
            used_wid_map={
                "pv28_4__content_o_1": "beleidskeuze-756",
                "pv28_4__content_o_2": "beleidskeuze-420",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-1-ref": "mock-ref-werkingsgebied-1",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-2-ref": "mock-ref-werkingsgebied-2",
            },
        )

    @pytest.fixture
    def gba_xml(self):
        mock_xml = """
        <Lichaam eId="body" wId="body">
            <Divisietekst eId="content_o_1" 
                wId="pv28_4__content_o_1"
                data-hint-object-code="beleidskeuze-756"
                data-hint-gebied-code="werkingsgebied-2">
                Lorem Ipsum Dolor Sit Amet.
                <IntIoRef eId="content_o_1__ref_o_1" 
                    wId="pv28_4__content_o_1__ref_o_1"
                    data-hint-locatie="werkingsgebied-1"
                    data-hint-gebiedengroep="Bodembeheergebied"
                    data-hint-gebiedsaanwijzingtype="Bodem">
                    Example Geo 2
                </IntIoRef>
                MockGebiedNaam
            </Divisietekst>
        </Lichaam>
        """
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(mock_xml.encode("utf-8"), parser)
        return root

    def test_build_annotation_map_gba(self, gba_xml):
        self.annotation_service._parse_data_hints(gba_xml)
        annotation_map = self.annotation_service.get_annotation_map()

        # Expecting one gebied annotation for the parent divisietekst/owtekstdeel
        # then a GBA annotation containing reference to wid and parent div
        expected_annotation_gebied = {
            "type_annotation": "gebied",
            "wid": "pv28_4__content_o_1",
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-756",
            "gebied_code": "werkingsgebied-2",
            "gebied_uuid": "20000000-0000-0005-0000-000000000002",
        }

        expected_gba_wid = "pv28_4__content_o_1__ref_o_1"
        expected_annotation_gebiedsaanwijzing = {
            "type_annotation": "gebiedsaanwijzing",
            "ref": "mock-ref-werkingsgebied-1",
            "werkingsgebied_code": "werkingsgebied-1",
            "groep": "Bodem",
            "type": "Bodembeheergebied",
            "parent_div": {
                "wid": "pv28_4__content_o_1",
                "object-code": "beleidskeuze-756",
                "gebied-code": "werkingsgebied-2",
                "uses_ambtsgebied": False,
            },
        }

        assert annotation_map["beleidskeuze-756"] == expected_annotation_gebied
        assert annotation_map[expected_gba_wid] == expected_annotation_gebiedsaanwijzing

    @pytest.fixture
    def gba_with_ambtsgebied_parent_xml(self):
        mock_xml = """
        <Lichaam eId="body" wId="body">
            <Divisietekst eId="content_o_1" 
                wId="pv28_4__content_o_1"
                data-hint-object-code="beleidskeuze-756"
                data-hint-ambtsgebied="True">
                Lorem Ipsum Dolor Sit Amet.
                <IntIoRef eId="content_o_1__ref_o_1" 
                    wId="pv28_4__content_o_1__ref_o_1"
                    data-hint-locatie="werkingsgebied-1"
                    data-hint-gebiedengroep="Bodembeheergebied"
                    data-hint-gebiedsaanwijzingtype="Bodem">
                    Example Geo 2
                </IntIoRef>
                MockGebiedNaam
            </Divisietekst>
        </Lichaam>
        """
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(mock_xml.encode("utf-8"), parser)
        return root

    def test_gba_with_ambtsgebied_parent(self, gba_with_ambtsgebied_parent_xml):
        self.annotation_service._parse_data_hints(gba_with_ambtsgebied_parent_xml)
        annotation_map = self.annotation_service.get_annotation_map()

        # Expecting 1x ambtsgebied annotation for the parent divisietekst/owtekstdeel
        # 1x GBA annotation
        expected_beleidskeuze = {
            "type_annotation": "ambtsgebied",
            "wid": "pv28_4__content_o_1",
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-756",
        }

        expected_gba_wid = "pv28_4__content_o_1__ref_o_1"
        expected_gba = {
            "type_annotation": "gebiedsaanwijzing",
            "ref": "mock-ref-werkingsgebied-1",
            "werkingsgebied_code": "werkingsgebied-1",
            "groep": "Bodem",
            "type": "Bodembeheergebied",
            "parent_div": {
                "wid": "pv28_4__content_o_1",
                "object-code": "beleidskeuze-756",
                "gebied-code": None,
                "uses_ambtsgebied": True,
            },
        }

        assert annotation_map["beleidskeuze-756"] == expected_beleidskeuze
        assert annotation_map[expected_gba_wid] == expected_gba

    @pytest.fixture
    def ambtsgebied_xml(self):
        mock_xml = """
        <Lichaam eId="body" wId="body">
            <Divisietekst eId="content_o_1"
                wId="pv28_4__content_o_1"
                data-hint-object-code="beleidskeuze-756"
                data-hint-ambtsgebied="True">
                Lorem Ipsum Dolor Sit Amet.
            </Divisietekst>
            <Divisietekst eId="content_o_2"
                wId="pv28_4__content_o_2"
                data-hint-object-code="beleidskeuze-420"
                data-hint-gebied-code="werkingsgebied-2">
                Lorem Ipsum Dolor Sit Amet.
            </Divisietekst>
        </Lichaam>
        """
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(mock_xml.encode("utf-8"), parser)
        return root

    def test_build_annotation_map_ambtsgebied_type(self, ambtsgebied_xml):
        self.annotation_service._parse_data_hints(ambtsgebied_xml)
        annotation_map = self.annotation_service.get_annotation_map()

        # ensure 1x ambtsgebied annotation and 1x gebied annotation
        expected_annotation_ambtsgebied = {
            "type_annotation": "ambtsgebied",
            "wid": "pv28_4__content_o_1",
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-756",
        }

        expected_annotation_gebied = {
            "type_annotation": "gebied",
            "wid": "pv28_4__content_o_2",
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-420",
            "gebied_code": "werkingsgebied-2",
            "gebied_uuid": "20000000-0000-0005-0000-000000000002",
        }

        assert annotation_map["beleidskeuze-756"] == expected_annotation_ambtsgebied
        assert annotation_map["beleidskeuze-420"] == expected_annotation_gebied
        print(annotation_map)

    def test_error_gebiedsaanwijzing_parent_divivisietest(self):
        parent = etree.Element(
            "RegelingOpschrift",  # unsupported element
            wId="pv28_4__content_o_2",
        )
        child = etree.Element("Inhoud")
        child2 = etree.Element("Al")

        # Create the child element with the required data-hint-* attributes
        gba = etree.SubElement(
            parent,
            "IntIoRef",
            wId="pv28_4__content_o_2__ref_o_1",
            **{
                "data-hint-locatie": "locatie",
                "data-hint-gebiedengroep": "groep",
                "data-hint-gebiedsaanwijzingtype": "type",
            }
        )
        child2.append(gba)
        child.append(child2)
        parent.append(child)

        with pytest.raises(ValueError):
            self.annotation_service._add_gebiedsaanwijzing_annotation(child)

    def test_multiple_gba_in_div(self):
        # TODO: add
        pass
