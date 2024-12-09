import pytest
from lxml import etree

from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object import PolicyObject
from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object_repository import PolicyObjectRepository
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

        self.policy_object_repository = PolicyObjectRepository()

        self.annotation_service = OWAnnotationService(
            policy_object_repository=self.policy_object_repository,
            werkingsgebied_repository=self.werkingsgebied_repository,
            used_wid_map={
                "beleidskeuze-1": "pv28_4__content_o_1",
                "beleidskeuze-2": "pv28_4__content_o_2",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-1-ref": "pv28_4__cmp_o_1__content_o_1__list_o_1__item_o_1__ref_o_1",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-2-ref": "pv28_4__cmp_o_1__content_o_1__list_o_1__item_o_3__ref_o_1",
            },
        )

    @pytest.fixture
    def gba_policy_object(self):
        hint_locatie = "werkingsgebied-1"
        hint_groep = "AandachtsgebiedLuchtkwaliteit"
        hint_type = "Lucht"
        
        gba = f'''<a data-hint-type="gebiedsaanwijzing" 
                   data-hint-gebiedengroep="{hint_groep}"
                   data-hint-locatie="{hint_locatie}"
                   data-hint-gebiedsaanwijzingtype="{hint_type}"
                   href="#">Testgebied 1</a>'''

        beleidskeuze_dict = {
            "UUID": "40000000-0000-0003-0000-000000000001",
            "Object_Type": "beleidskeuze",
            "Object_ID": 1,
            "Code": "beleidskeuze-1",
            "Hierarchy_Code": "beleidsdoel-1",
            "Werkingsgebied_Code": "werkingsgebied-2",
            "Title": "Mock beleidskeuze with Gebiedsaanwijzing and gebied annotations",
            "Description": f"<p>Lorem ipsum {gba} dolor sit amet, consectetur adipiscing elit.<p>",
            "Cause": None,
            "Provincial_Interest": None,
            "Explanation": None,
            "Role": None,
            "Effect": None,
            "Themas": None,
            "Hoofdlijnen": None,
        }
        return beleidskeuze_dict

    def test_build_annotation_map_gba(self, gba_policy_object):
        self.policy_object_repository.add("beleidskeuze-1", gba_policy_object)
        self.annotation_service.build_annotation_map()
        annotation_map = self.annotation_service.get_annotation_map()

        # Expecting one gebied annotation and one GBA annotation under the same object_code
        expected_annotations = [
            {
                "type_annotation": "gebied",
                "wid": "pv28_4__content_o_1",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-1",
                "gebied_code": "werkingsgebied-2",
                "gio_ref": "0ebf544d-5f58-4cd0-82ff-f5941081d746",
            },
            {
                "type_annotation": "gebiedsaanwijzing",
                "tag": "IntIoRef",
                "wid": "hark",
                "werkingsgebied_code": "werkingsgebied-1",
                "groep": "AandachtsgebiedLuchtkwaliteit",
                "type": "Lucht",
                "parent_div": {
                    "wid": "pv28_4__content_o_1",
                    "object-code": "beleidskeuze-1",
                    "gebied-code": "werkingsgebied-2",
                    "uses_ambtsgebied": False,
                },
            }
        ]

        assert annotation_map["beleidskeuze-1"] == expected_annotations

    # @pytest.fixture
    # def gba_with_ambtsgebied_parent_xml(self):
    #     mock_xml = """
    #     <Lichaam eId="body" wId="body">
    #         <Divisietekst eId="content_o_1" 
    #             wId="pv28_4__content_o_1"
    #             data-hint-object-code="beleidskeuze-756"
    #             data-hint-ambtsgebied="True">
    #             Lorem Ipsum Dolor Sit Amet.
    #             <IntIoRef eId="content_o_1__ref_o_1" 
    #                 wId="pv28_4__content_o_1__ref_o_1"
    #                 data-hint-locatie="werkingsgebied-1"
    #                 data-hint-gebiedengroep="Bodembeheergebied"
    #                 data-hint-gebiedsaanwijzingtype="Bodem">
    #                 Example Geo 2
    #             </IntIoRef>
    #             MockGebiedNaam
    #         </Divisietekst>
    #     </Lichaam>
    #     """
    #     parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
    #     root = etree.fromstring(mock_xml.encode("utf-8"), parser)
    #     return root

    # def test_gba_with_ambtsgebied_parent(self, gba_with_ambtsgebied_parent_xml):
    #     self.annotation_service._parse_data_hints(gba_with_ambtsgebied_parent_xml)
    #     annotation_map = self.annotation_service.get_annotation_map()

    #     expected_annotations = [
    #         {
    #             "type_annotation": "ambtsgebied",
    #             "wid": "pv28_4__content_o_1",
    #             "tag": "Divisietekst",
    #             "object_code": "beleidskeuze-756",
    #         },
    #         {
    #             "type_annotation": "gebiedsaanwijzing",
    #             "tag": "IntIoRef",
    #             "ref": "mock-ref-werkingsgebied-1",
    #             "wid": "pv28_4__content_o_1__ref_o_1",
    #             "werkingsgebied_code": "werkingsgebied-1",
    #             "groep": "Bodembeheergebied",
    #             "type": "Bodem",
    #             "parent_div": {
    #                 "wid": "pv28_4__content_o_1",
    #                 "object-code": "beleidskeuze-756",
    #                 "gebied-code": None,
    #                 "uses_ambtsgebied": True,
    #             },
    #         }
    #     ]

    #     assert annotation_map["beleidskeuze-756"] == expected_annotations

    # @pytest.fixture
    # def ambtsgebied_xml(self):
    #     mock_xml = """
    #     <Lichaam eId="body" wId="body">
    #         <Divisietekst eId="content_o_1"
    #             wId="pv28_4__content_o_1"
    #             data-hint-object-code="beleidskeuze-756"
    #             data-hint-ambtsgebied="True">
    #             Lorem Ipsum Dolor Sit Amet.
    #         </Divisietekst>
    #         <Divisietekst eId="content_o_2"
    #             wId="pv28_4__content_o_2"
    #             data-hint-object-code="beleidskeuze-420"
    #             data-hint-gebied-code="werkingsgebied-2">
    #             Lorem Ipsum Dolor Sit Amet.
    #         </Divisietekst>
    #     </Lichaam>
    #     """
    #     parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
    #     root = etree.fromstring(mock_xml.encode("utf-8"), parser)
    #     return root

    # def test_build_annotation_map_ambtsgebied_type(self, ambtsgebied_xml):
    #     self.annotation_service._parse_data_hints(ambtsgebied_xml)
    #     annotation_map = self.annotation_service.get_annotation_map()

    #     # Each object_code should have a single annotation in its list
    #     expected_annotations_756 = [{
    #         "type_annotation": "ambtsgebied",
    #         "wid": "pv28_4__content_o_1",
    #         "tag": "Divisietekst",
    #         "object_code": "beleidskeuze-756",
    #     }]

    #     expected_annotations_420 = [{
    #         "type_annotation": "gebied",
    #         "wid": "pv28_4__content_o_2",
    #         "tag": "Divisietekst",
    #         "object_code": "beleidskeuze-420",
    #         "gebied_code": "werkingsgebied-2",
    #         "gio_ref": "0ebf544d-5f58-4cd0-82ff-f5941081d746",
    #     }]

    #     assert annotation_map["beleidskeuze-756"] == expected_annotations_756
    #     assert annotation_map["beleidskeuze-420"] == expected_annotations_420

    # def test_error_gebiedsaanwijzing_parent_divivisietest(self):
    #     parent = etree.Element(
    #         "RegelingOpschrift",  # unsupported element
    #         wId="pv28_4__content_o_2",
    #     )
    #     child = etree.Element("Inhoud")
    #     child2 = etree.Element("Al")

    #     # Create the child element with the required data-hint-* attributes
    #     gba = etree.SubElement(
    #         parent,
    #         "IntIoRef",
    #         wId="pv28_4__content_o_2__ref_o_1",
    #         **{
    #             "data-hint-locatie": "locatie",
    #             "data-hint-gebiedengroep": "groep",
    #             "data-hint-gebiedsaanwijzingtype": "type",
    #         }
    #     )
    #     child2.append(gba)
    #     child.append(child2)
    #     parent.append(child)

    #     with pytest.raises(ValueError):
    #         self.annotation_service._add_gebiedsaanwijzing_annotation(child)

    # def test_multiple_gba_in_div(self):
    #     # TODO: add
    #     pass

    # @pytest.fixture
    # def thema_hoofdlijn_annotations_xml(self):
    #     """
    #     Test if the annotation service correctly parses the data-hint-* attributes
    #     for thema, hoofdlijn and ambtsgebied.
    #     """
    #     mock_xml = """
    #     <Lichaam eId="body" wId="body">
    #         <Divisietekst eId="content_o_1"
    #             wId="pv28_4__content_o_1"
    #             data-hint-object-code="beleidskeuze-756"
    #             data-hint-themas="geluid"
    #             data-hint-hoofdlijnen="omgevingsvisie|Example Value 1"
    #             data-hint-ambtsgebied="True">
    #             single thema and hoofdlijn used
    #         </Divisietekst>
    #         <Divisietekst eId="content_o_2"
    #             wId="pv28_4__content_o_2"
    #             data-hint-object-code="beleidskeuze-888"
    #             data-hint-themas="bodem,water"
    #             data-hint-hoofdlijnen="omgevingsvisie|Example Value 1,omgevingsvisie|Example Value 2"
    #             data-hint-ambtsgebied="True">
    #             multiple themas and hoofdlijnen used
    #         </Divisietekst>
    #     </Lichaam>
    #     """
    #     parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
    #     root = etree.fromstring(mock_xml.encode("utf-8"), parser)
    #     return root

    # def test_total_annotations(self, thema_hoofdlijn_annotations_xml):
    #     self.annotation_service._parse_data_hints(thema_hoofdlijn_annotations_xml)
    #     annotation_map = self.annotation_service.get_annotation_map()
    #     assert len(annotation_map) == 2

    # def test_build_annotation_map_single_thema_hoofdlijn(self, thema_hoofdlijn_annotations_xml):
    #     self.annotation_service._parse_data_hints(thema_hoofdlijn_annotations_xml)
    #     annotation_map = self.annotation_service.get_annotation_map()

    #     expected_annotations = [
    #         {
    #             "type_annotation": "ambtsgebied",
    #             "tag": "Divisietekst", 
    #             "wid": "pv28_4__content_o_1",
    #             "object_code": "beleidskeuze-756",
    #         },
    #         {
    #             "type_annotation": "thema",
    #             "tag": "Divisietekst",
    #             "wid": "pv28_4__content_o_1", 
    #             "object_code": "beleidskeuze-756",
    #             "thema_waardes": ["geluid"],
    #         },
    #         {
    #             "type_annotation": "hoofdlijn",
    #             "tag": "Divisietekst",
    #             "wid": "pv28_4__content_o_1",
    #             "object_code": "beleidskeuze-756",
    #             "hoofdlijnen": [{'soort': 'omgevingsvisie', 'naam': 'Example Value 1'}],
    #         }
    #     ]

    #     assert annotation_map["beleidskeuze-756"] == expected_annotations

    # def test_build_annotation_map_multiple_themas_hoofdlijnen(self, thema_hoofdlijn_annotations_xml):
    #     self.annotation_service._parse_data_hints(thema_hoofdlijn_annotations_xml)
    #     annotation_map = self.annotation_service.get_annotation_map()

    #     expected_annotations = [
    #         {
    #             "type_annotation": "ambtsgebied",
    #             "wid": "pv28_4__content_o_2",
    #             "tag": "Divisietekst",
    #             "object_code": "beleidskeuze-888",
    #         },
    #         {
    #             "type_annotation": "thema",
    #             "tag": "Divisietekst",
    #             "wid": "pv28_4__content_o_2",
    #             "object_code": "beleidskeuze-888",
    #             "thema_waardes": [
    #                 "bodem",
    #                 "water"
    #             ],
    #         },
    #         {
    #             "type_annotation": "hoofdlijn",
    #             "tag": "Divisietekst",
    #             "wid": "pv28_4__content_o_2",
    #             "object_code": "beleidskeuze-888",
    #             "hoofdlijnen": [
    #                 {'soort': 'omgevingsvisie', 'naam': 'Example Value 1'},
    #                 {'soort': 'omgevingsvisie', 'naam': 'Example Value 2'}
    #             ],
    #         }
    #     ]

    #     assert annotation_map["beleidskeuze-888"] == expected_annotations
