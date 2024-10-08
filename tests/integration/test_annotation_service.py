from pathlib import Path
import json
import pytest

from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from dso.services.ow.ow_annotation_service import OWAnnotationService


class TestOWAnnotationService:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize common resources."""
        # Load Werkingsgebied data from a JSON file and populate the repository
        json_file_path = Path(__file__).parent.parent / "fixtures/werkingsgebied-example.json"
        with open(json_file_path, "r") as f:
            werkingsgebied_data = json.load(f)

        self.werkingsgebied_repository = WerkingsgebiedRepository()
        self.werkingsgebied_repository.add_from_dict(werkingsgebied_data)

        self.annotation_service = OWAnnotationService(
            werkingsgebied_repository=self.werkingsgebied_repository,
            used_wid_map={
                "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7": "beleidskeuze-756",
                "pv28_4__div_o_2__div_o_16__div_o_1__content_o_8": "beleidskeuze-420",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-1-ref": "mock-ref-werkingsgebied-1",
                "bijlage-werkingsgebieden-divisietekst-referentie-werkingsgebied-2-ref": "mock-ref-werkingsgebied-2",
            },
        )

    @pytest.fixture
    def gba_xml(self):
        xml_file_path = Path(__file__).parent.parent / "fixtures/vrijetekst-simple-gba.xml"
        with open(xml_file_path, "r", encoding="utf-8") as f:
            return f.read()

    @pytest.fixture
    def ambtsgebied_xml(self):
        xml_file_path = Path(__file__).parent.parent / "fixtures/vrijetekst-simple-ambtsgebied.xml"
        with open(xml_file_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_build_annotation_map_gba(self, gba_xml):
        # Process the sample XML
        output_xml = self.annotation_service.build_annotation_map(gba_xml)

        # Check the resulting annotation map
        annotation_map = self.annotation_service.get_annotation_map()

        # Expecting one gebied annotation for the parent divisietekst/owtekstdeel
        # then a GBA annotation containing reference to wid and parent div
        expected_annotation_map = {
            "beleidskeuze-756": {
                "type_annotation": "gebied",
                "wid": "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-756",
                "gebied_code": "werkingsgebied-2",
                "gebied_uuid": "20000000-0000-0005-0000-000000000002",
            },
            "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7__ref_o_1": {
                "type_annotation": "gebiedsaanwijzing",
                "ref": "mock-ref-werkingsgebied-1",
                "werkingsgebied_code": "werkingsgebied-1",
                "groep": "Bodem",
                "type": "Bodembeheergebied",
                "parent_div": {
                    "wid": "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7",
                    "object-code": "beleidskeuze-756",
                    "gebied-code": "werkingsgebied-2",
                },
            },
        }

        assert annotation_map == expected_annotation_map

    def test_build_annotation_map_ambtsgebied_type(self, ambtsgebied_xml):
        # Process the alternative XML
        output_xml = self.annotation_service.build_annotation_map(ambtsgebied_xml)

        # Check the resulting annotation map
        annotation_map = self.annotation_service.get_annotation_map()

        expected_annotation_map = {
            "beleidskeuze-756": {
                "type_annotation": "ambtsgebied",
                "wid": "pv28_4__div_o_2__div_o_16__div_o_1__content_o_7",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-756",
            },
            "beleidskeuze-420": {
                "type_annotation": "gebied",
                "wid": "pv28_4__div_o_2__div_o_16__div_o_1__content_o_8",
                "tag": "Divisietekst",
                "object_code": "beleidskeuze-420",
                "gebied_code": "werkingsgebied-2",
                "gebied_uuid": "20000000-0000-0005-0000-000000000002",
            },
        }

        assert annotation_map == expected_annotation_map
