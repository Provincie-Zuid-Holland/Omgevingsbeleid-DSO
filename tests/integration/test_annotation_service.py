import pytest
from lxml import etree

from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from dso.services.ow.ow_annotation_service import OWAnnotationService


class TestOWAnnotationService:
    @pytest.fixture(autouse=True)
    def setup_method(self, input_data_werkingsgebieden):
        """Setup method to initialize common resources."""
        self.werkingsgebied_repository = WerkingsgebiedRepository()
        self.werkingsgebied_repository.add_from_dict(input_data_werkingsgebieden)

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
                    Gebiedsaanwijzing MockGebied1
                </IntIoRef>
            </Divisietekst>
        </Lichaam>
        """
        parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
        root = etree.fromstring(mock_xml.encode("utf-8"), parser)
        return root

    def test_build_annotation_map_gba(self, gba_xml):
        self.annotation_service._parse_data_hints(gba_xml)
        annotation_map = self.annotation_service.get_annotation_map()

        # Expecting one gebied annotation and one GBA annotation under the same object_code
        expected_annotations = [
            {
                "type_annotation": "gebied",
                "wid": "pv28_4__content_o_1",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-756",
                "gebied_code": "werkingsgebied-2",
                "gio_ref": "wg-1-00000000-0000-0005-0000-000000000002",
            },
            {
                "type_annotation": "gebiedsaanwijzing",
                "tag": "IntIoRef",
                "ref": "mock-ref-werkingsgebied-1",
                "wid": "pv28_4__content_o_1__ref_o_1",
                "werkingsgebied_code": "werkingsgebied-1",
                "groep": "Bodembeheergebied",
                "type": "Bodem",
                "parent_div": {
                    "wid": "pv28_4__content_o_1",
                    "object-code": "beleidskeuze-756",
                    "gebied-code": "werkingsgebied-2",
                    "uses_ambtsgebied": False,
                },
            }
        ]

        assert annotation_map["beleidskeuze-756"] == expected_annotations

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

        expected_annotations = [
            {
                "type_annotation": "ambtsgebied",
                "wid": "pv28_4__content_o_1",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-756",
            },
            {
                "type_annotation": "gebiedsaanwijzing",
                "tag": "IntIoRef",
                "ref": "mock-ref-werkingsgebied-1",
                "wid": "pv28_4__content_o_1__ref_o_1",
                "werkingsgebied_code": "werkingsgebied-1",
                "groep": "Bodembeheergebied",
                "type": "Bodem",
                "parent_div": {
                    "wid": "pv28_4__content_o_1",
                    "object-code": "beleidskeuze-756",
                    "gebied-code": None,
                    "uses_ambtsgebied": True,
                },
            }
        ]

        assert annotation_map["beleidskeuze-756"] == expected_annotations

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

        # Each object_code should have a single annotation in its list
        expected_annotations_756 = [{
            "type_annotation": "ambtsgebied",
            "wid": "pv28_4__content_o_1",
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-756",
        }]

        expected_annotations_420 = [{
            "type_annotation": "gebied",
            "wid": "pv28_4__content_o_2",
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-420",
            "gebied_code": "werkingsgebied-2",
            "gio_ref": "wg-1-00000000-0000-0005-0000-000000000002",
        }]

        assert annotation_map["beleidskeuze-756"] == expected_annotations_756
        assert annotation_map["beleidskeuze-420"] == expected_annotations_420

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
