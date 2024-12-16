from uuid import UUID

import pytest

from dso.act_builder.services.ow.ow_builder_context import BuilderContext
from dso.act_builder.services.ow.ow_hoofdlijnen import OwHoofdlijnBuilder
from dso.act_builder.state_manager.states.ow_repository import OWStateRepository
from dso.models import OwData
from dso.services.ow import (
    OWDivisieTekst,
    OWTekstdeel,
)
from dso.services.ow.models import OWHoofdlijn


class TestOWHoofdlijnBuilder:
    @pytest.fixture()
    def mock_ow_objects(self):
        mock_divisie_1 = OWDivisieTekst(
            OW_ID="nl.imow-pv28.divisie.01",
            wid="pv28_4__content_o_1",
            mapped_policy_object_code="beleidskeuze-1",
        )
        mock_tekstdeel_1 = OWTekstdeel(
            OW_ID="nl.imow-pv28.tekstdeel.01",
            divisie=mock_divisie_1.OW_ID,
            hoofdlijnen=[],
            themas=[],
        )
        mock_divisie_2 = OWDivisieTekst(
            OW_ID="nl.imow-pv28.divisie.02",
            wid="pv28_4__content_o_2",
            mapped_policy_object_code="beleidskeuze-2",
        )
        mock_tekstdeel_2 = OWTekstdeel(
            OW_ID="nl.imow-pv28.tekstdeel.02",
            divisie=mock_divisie_2.OW_ID,
            hoofdlijnen=[],
            themas=[],
        )
        mock_divisie_3 = OWDivisieTekst(
            OW_ID="nl.imow-pv28.divisie.03",
            wid="pv28_4__content_o_3",
            mapped_policy_object_code="beleidskeuze-3",
        )
        mock_tekstdeel_3 = OWTekstdeel(
            OW_ID="nl.imow-pv28.tekstdeel.03",
            divisie=mock_divisie_3.OW_ID,
            hoofdlijnen=[],
            themas=[],
        )

        return [
            mock_divisie_1,
            mock_tekstdeel_1,
            mock_divisie_2,
            mock_tekstdeel_2,
            mock_divisie_3,
            mock_tekstdeel_3,
        ]

    @pytest.fixture()
    def mock_ow_data(self, mock_ow_objects):
        mock_ow_data = OwData(
            ow_objects={},
            terminated_ow_ids=[],
        )

        for obj in mock_ow_objects:
            mock_ow_data.ow_objects[obj.OW_ID] = obj

        return mock_ow_data

    @pytest.fixture(autouse=True)
    def setup_method(self, mock_ow_data: OwData, mock_ow_objects):
        """Setup method to initialize common resources."""
        self.context = BuilderContext(
            provincie_id="pv28",
            ow_procedure_status=None,
            levering_id="10000000-0000-0000-0000-000000000001",
            orphaned_wids=[],
        )

        self.annotation_lookup_map = {
            "beleidskeuze-1": [
                {
                    "type_annotation": "ambtsgebied",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_1",
                    "object_code": "beleidskeuze-1",
                },
                {
                    "type_annotation": "thema",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_1",
                    "object_code": "beleidskeuze-1",
                    "thema_waardes": ["geluid"],
                },
                {
                    "type_annotation": "hoofdlijn",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_1",
                    "object_code": "beleidskeuze-1",
                    "hoofdlijnen": [{"soort": "hoofdlijn_soort1", "naam": "Example Value 1"}],
                },
            ],
            "beleidskeuze-2": [
                {
                    "type_annotation": "ambtsgebied",
                    "wid": "pv28_4__content_o_2",
                    "tag": "Divisietekst",
                    "object_code": "beleidskeuze-2",
                },
                {
                    "type_annotation": "thema",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_2",
                    "object_code": "beleidskeuze-2",
                    "thema_waardes": ["bodem", "water"],
                },
                {
                    "type_annotation": "hoofdlijn",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_2",
                    "object_code": "beleidskeuze-2",
                    "hoofdlijnen": [
                        {"soort": "hoofdlijn_soort1", "naam": "Example Value 2"},
                        {"soort": "hoofdlijn_soort1", "naam": "Example Value 3"},
                    ],
                },
            ],
            "beleidskeuze-3": [
                {
                    "type_annotation": "ambtsgebied",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_3",
                    "object_code": "beleidskeuze-3",
                },
                {
                    "type_annotation": "hoofdlijn",
                    "tag": "Divisietekst",
                    "wid": "pv28_4__content_o_3",
                    "object_code": "beleidskeuze-3",
                    "hoofdlijnen": [{"soort": "hoofdlijn_soort1", "naam": "Example Value 1"}],
                },
            ],
        }

        self.ow_repository = OWStateRepository(ow_input_data=mock_ow_data)
        self.builder = OwHoofdlijnBuilder(
            context=self.context, annotation_lookup_map=self.annotation_lookup_map, ow_repository=self.ow_repository
        )

    def test_builder_init(self):
        assert self.builder._context == self.context
        # ensure filter correct - should find 2 hoofdlijn annotations
        assert len(self.builder._annotation_lookup) == 3
        assert self.builder._ow_repository == self.ow_repository

    def test_handle_ow_objects_creates_new_hoofdlijnen(self, mock_ow_objects):
        """Test that new hoofdlijnen objects are created correctly"""
        self.builder.handle_ow_object_changes()

        new_objects = self.ow_repository._new_ow_objects
        assert len(new_objects) == 3  # 3 unique hoofdlijnen across both tekstdelen

        for hoofdlijn in new_objects:
            assert isinstance(hoofdlijn, OWHoofdlijn)
            assert hoofdlijn.soort == "hoofdlijn_soort1"
            assert hoofdlijn.naam in ["Example Value 1", "Example Value 2", "Example Value 3"]

    def test_handle_ow_objects_updates_tekstdeel_with_single_hoofdlijn(self, mock_ow_objects):
        """Test that tekstdelen with single hoofdlijn are updated correctly"""
        self.builder.handle_ow_object_changes()

        mutated_objects = self.ow_repository._mutated_ow_objects
        new_objects = self.ow_repository._new_ow_objects

        tekstdeel_1 = mutated_objects[0]  # beleidskeuze-1
        assert isinstance(tekstdeel_1, OWTekstdeel)
        assert len(tekstdeel_1.hoofdlijnen) == 1
        assert tekstdeel_1.hoofdlijnen[0] == new_objects[0].OW_ID

        tekstdeel_3 = mutated_objects[2]  # beleidskeuze-3
        assert isinstance(tekstdeel_3, OWTekstdeel)
        assert len(tekstdeel_3.hoofdlijnen) == 1
        assert tekstdeel_3.hoofdlijnen[0] == new_objects[0].OW_ID  # reuses existing hoofdlijn

    def test_handle_ow_objects_updates_tekstdeel_with_multiple_hoofdlijnen(self, mock_ow_objects):
        """Test that tekstdelen with multiple hoofdlijnen are updated correctly"""
        self.builder.handle_ow_object_changes()

        mutated_objects = self.ow_repository._mutated_ow_objects
        new_objects = self.ow_repository._new_ow_objects

        tekstdeel_2 = mutated_objects[1]  # beleidskeuze-2
        assert isinstance(tekstdeel_2, OWTekstdeel)
        assert len(tekstdeel_2.hoofdlijnen) == 2
        assert all(h_id in [obj.OW_ID for obj in new_objects] for h_id in tekstdeel_2.hoofdlijnen)
