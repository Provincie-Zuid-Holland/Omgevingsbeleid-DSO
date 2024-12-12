import pytest
from lxml import etree

from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object import PolicyObject
from dso.act_builder.state_manager.input_data.resource.policy_object.policy_object_repository import (
    PolicyObjectRepository,
)
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
                "beleidskeuze-1-gebiedsaanwijzing-1": "pv28_4__content_o_1__ref_o_1",
                "beleidskeuze-2": "pv28_4__content_o_2",
                "beleidskeuze-3": "pv28_4__content_o_3",
                "beleidskeuze-4": "pv28_4__content_o_4",
                "beleidskeuze-4-gebiedsaanwijzing-1": "pv28_4__content_o_4__ref_o_1",
                "beleidskeuze-4-gebiedsaanwijzing-2": "pv28_4__content_o_4__ref_o_2",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-1-ref": "pv28_4__cmp_o_1__content_o_1__list_o_1__item_o_1__ref_o_1",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-2-ref": "pv28_4__cmp_o_1__content_o_1__list_o_1__item_o_3__ref_o_1",
            },
        )

    @pytest.fixture
    def gba_policy_object(self):
        hint_locatie = "werkingsgebied-1"
        hint_groep = "AandachtsgebiedLuchtkwaliteit"
        hint_type = "Lucht"

        gba = f"""<a data-hint-type="gebiedsaanwijzing" 
                   data-hint-gebiedengroep="{hint_groep}"
                   data-hint-locatie="{hint_locatie}"
                   data-hint-gebiedsaanwijzingtype="{hint_type}"
                   href="#">Testgebied 1</a>"""

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
                "wid": "pv28_4__content_o_1__ref_o_1",
                "werkingsgebied_code": "werkingsgebied-1",
                "groep": "AandachtsgebiedLuchtkwaliteit",
                "type": "Lucht",
                "parent_div": {
                    "wid": "pv28_4__content_o_1",
                    "object-code": "beleidskeuze-1",
                    "gebied-code": "werkingsgebied-2",
                    "uses_ambtsgebied": False,
                },
            },
        ]

        assert annotation_map["beleidskeuze-1"] == expected_annotations

    # @pytest.fixture
    # def gba_policy_object_with_wrong_type(self, gba_policy_object):
    #     hint_groep_1 = "AandachtsgebiedLuchtkwaliteit"
    #     hint_locatie_1 = "werkingsgebied-1"
    #     hint_type_1 = "Lucht"

    #     gba = f"""<a data-hint-type="gebiedsaanwijzing" 
    #                data-hint-gebiedengroep="{hint_groep_1}"
    #                data-hint-locatie="{hint_locatie_1}"
    #                data-hint-gebiedsaanwijzingtype="{hint_type_1}"
    #                href="#">Testgebied 1</a>"""

    #     gba_policy_object["Description"] = f"<p>Lorem ipsum {gba} dolor sit amet, consectetur adipiscing elit.<p>"

    #     return gba_policy_object

    # def test_fail_annotation_map_gba_type(self, gba_policy_object_with_wrong_type):
    #     self.policy_object_repository.add("beleidskeuze-1", gba_policy_object_with_wrong_type)

    #     # TODO: raise validation error again
    #     with pytest.raises(ValueError):
    #         self.annotation_service.build_annotation_map()

    @pytest.fixture
    def policy_object_with_ambtsgebied(self):
        beleidskeuze_dict = {
            "UUID": "40000000-0000-0003-0000-000000000003",
            "Object_Type": "beleidskeuze",
            "Object_ID": 3,
            "Code": "beleidskeuze-3",
            "Hierarchy_Code": "beleidsdoel-1",
            "Werkingsgebied_Code": None,
            "Title": "Mock beleidskeuze with ambtsgebied annotations",
            "Description": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.<p>",
            "Cause": None,
            "Provincial_Interest": None,
            "Explanation": None,
            "Role": None,
            "Effect": None,
            "Themas": None,
            "Hoofdlijnen": None,
        }
        return beleidskeuze_dict

    def test_build_annotation_map_ambtsgebied(self, policy_object_with_ambtsgebied):
        self.policy_object_repository.add("beleidskeuze-3", policy_object_with_ambtsgebied)
        self.annotation_service.build_annotation_map()
        annotation_map = self.annotation_service.get_annotation_map()

        # Expecting one ambtsgebied annotation
        expected_annotations = [
            {
                "type_annotation": "ambtsgebied",
                "wid": "pv28_4__content_o_3",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-3",
            }
        ]

        assert annotation_map["beleidskeuze-3"] == expected_annotations

    @pytest.fixture
    def policy_object_with_gebied_annotation(self):
        beleidskeuze_dict = {
            "UUID": "40000000-0000-0003-0000-000000000002",
            "Object_Type": "beleidskeuze",
            "Object_ID": 2,
            "Code": "beleidskeuze-2",
            "Hierarchy_Code": "beleidsdoel-1",
            "Werkingsgebied_Code": "werkingsgebied-2",
            "Title": "Mock beleidskeuze with gebied annotation",
            "Description": "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.<p>",
            "Cause": None,
            "Provincial_Interest": None,
            "Explanation": None,
            "Role": None,
            "Effect": None,
            "Themas": None,
            "Hoofdlijnen": None,
        }
        return beleidskeuze_dict

    def test_build_annotation_map_gebied_annotation(self, policy_object_with_gebied_annotation):
        self.policy_object_repository.add("beleidskeuze-2", policy_object_with_gebied_annotation)
        self.annotation_service.build_annotation_map()
        annotation_map = self.annotation_service.get_annotation_map()

        # expecting one gebied annotation
        expected_annotations = [
            {
                "type_annotation": "gebied",
                "wid": "pv28_4__content_o_2",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-2",
                "gebied_code": "werkingsgebied-2",
                "gio_ref": "0ebf544d-5f58-4cd0-82ff-f5941081d746",
            }
        ]

        assert annotation_map["beleidskeuze-2"] == expected_annotations

    @pytest.fixture
    def multiple_gba_policy_object(self):
        hint_locatie_1 = "werkingsgebied-1"
        hint_groep_1 = "AandachtsgebiedLuchtkwaliteit"
        hint_type_1 = "Lucht"

        gba_1 = f"""<a data-hint-type="gebiedsaanwijzing" 
                   data-hint-gebiedengroep="{hint_groep_1}"
                   data-hint-locatie="{hint_locatie_1}"
                   data-hint-gebiedsaanwijzingtype="{hint_type_1}"
                   href="#">Testgebied 1</a>"""

        hint_locatie_2 = "werkingsgebied-2"
        hint_groep_2 = "AandachtsgebiedLuchtkwaliteit"
        hint_type_2 = "Lucht"

        gba_2 = f"""<a data-hint-type="gebiedsaanwijzing" 
                   data-hint-gebiedengroep="{hint_groep_2}"
                   data-hint-locatie="{hint_locatie_2}"
                   data-hint-gebiedsaanwijzingtype="{hint_type_2}"
                   href="#">Testgebied 2</a>"""

        beleidskeuze_dict = {
            "UUID": "40000000-0000-0003-0000-000000000004",
            "Object_Type": "beleidskeuze",
            "Object_ID": 4,
            "Code": "beleidskeuze-4",
            "Hierarchy_Code": "beleidsdoel-1",
            "Werkingsgebied_Code": None,  # ambtsgebied
            "Title": "Mock beleidskeuze with multiple gba annotation",
            "Description": f"<p>Lorem ipsum {gba_1} dolor sit amet, consectetur {gba_2} adipiscing elit.<p>",
        }
        return beleidskeuze_dict

    def test_multiple_gba_in_div(self, multiple_gba_policy_object):
        self.policy_object_repository.add("beleidskeuze-4", multiple_gba_policy_object)
        self.annotation_service.build_annotation_map()
        annotation_map = self.annotation_service.get_annotation_map()

        expected_annotation_1 = {
            "type_annotation": "gebiedsaanwijzing",
            "tag": "IntIoRef",
            "wid": "pv28_4__content_o_4__ref_o_1",
            "werkingsgebied_code": "werkingsgebied-1",
            "groep": "AandachtsgebiedLuchtkwaliteit",
            "type": "Lucht",
            "parent_div": {
                "wid": "pv28_4__content_o_4",
                "object-code": "beleidskeuze-4",
                "gebied-code": None,
                "uses_ambtsgebied": True,
            },
        }
        expected_annotation_2 = {
            "type_annotation": "gebiedsaanwijzing",
            "tag": "IntIoRef",
            "wid": "pv28_4__content_o_4__ref_o_2",
            "werkingsgebied_code": "werkingsgebied-2",
            "groep": "AandachtsgebiedLuchtkwaliteit",
            "type": "Lucht",
            "parent_div": {
                "wid": "pv28_4__content_o_4",
                "object-code": "beleidskeuze-4",
                "gebied-code": None,
                "uses_ambtsgebied": True,
            },
        }

        assert len(annotation_map["beleidskeuze-4"]) == 3
        assert annotation_map["beleidskeuze-4"][1] == expected_annotation_1
        assert annotation_map["beleidskeuze-4"][2] == expected_annotation_2

    @pytest.fixture
    def policy_object_with_hoofdlijn_annotation(self, policy_object_with_ambtsgebied):
        policy_object_with_ambtsgebied["Hoofdlijnen"] = [
            {"soort": "omgevingsvisie", "naam": "Mock Hoofdlijn Value"},
            {"soort": "omgevingsvisie", "naam": "Example Hoofdlijn 2"},
        ]
        return policy_object_with_ambtsgebied

    def test_build_annotation_map_hoofdlijn(self, policy_object_with_hoofdlijn_annotation):
        self.policy_object_repository.add("beleidskeuze-3", policy_object_with_hoofdlijn_annotation)
        self.annotation_service.build_annotation_map()
        annotation_map = self.annotation_service.get_annotation_map()

        expected_hoofdlijn = {
            "type_annotation": "hoofdlijn",
            "tag": "Divisietekst",
            "wid": "pv28_4__content_o_3",
            "object_code": "beleidskeuze-3",
            "hoofdlijnen": [
                {"soort": "omgevingsvisie", "naam": "Mock Hoofdlijn Value"},
                {"soort": "omgevingsvisie", "naam": "Example Hoofdlijn 2"},
            ],
        }
        assert len(annotation_map["beleidskeuze-3"]) == 2
        assert annotation_map["beleidskeuze-3"][1] == expected_hoofdlijn

    @pytest.fixture
    def policy_object_with_thema_annotation(self, policy_object_with_ambtsgebied):
        policy_object_with_ambtsgebied["Themas"] = [
            "bodem",
            "water",
        ]
        return policy_object_with_ambtsgebied

    def test_build_annotation_map_thema(self, policy_object_with_thema_annotation):
        self.policy_object_repository.add("beleidskeuze-3", policy_object_with_thema_annotation)
        self.annotation_service.build_annotation_map()
        annotation_map = self.annotation_service.get_annotation_map()

        expected_thema = {
            "type_annotation": "thema",
            "tag": "Divisietekst",
            "wid": "pv28_4__content_o_3",
            "object_code": "beleidskeuze-3",
            "thema_waardes": [
                "bodem",
                "water",
            ],
        }
        assert len(annotation_map["beleidskeuze-3"]) == 2
        assert annotation_map["beleidskeuze-3"][1] == expected_thema

    # @pytest.fixture
    # def policy_object_invalid_thema_annotation(self, policy_object_with_ambtsgebied):
    #     policy_object_with_ambtsgebied["Themas"] = ["noexist"]
    #     return policy_object_with_ambtsgebied

    # def test_fail_annotation_map_thema(self, policy_object_invalid_thema_annotation):
    #     self.policy_object_repository.add("beleidskeuze-3", policy_object_invalid_thema_annotation)

    #     with pytest.raises(ValueError):
    #         self.annotation_service.build_annotation_map()
