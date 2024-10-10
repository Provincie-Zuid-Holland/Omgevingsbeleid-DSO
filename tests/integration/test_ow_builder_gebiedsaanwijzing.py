from uuid import UUID

import pytest

from dso.act_builder.services.ow.ow_builder_context import BuilderContext
from dso.act_builder.services.ow.ow_gebiedsaanwijzingen import OwGebiedsaanwijzingBuilder
from dso.act_builder.state_manager.states.ow_repository import OWStateRepository
from dso.models import OwData
from dso.services.ow import (
    BestuurlijkeGrenzenVerwijzing,
    OWAmbtsgebied,
    OWDivisie,
    OWGebied,
    OWGebiedenGroep,
    OWRegelingsgebied,
    OWTekstdeel,
)
from dso.services.ow.models import OWGebiedsaanwijzing


class TestOWGebiedsaanwijzingBuilder:
    @pytest.fixture()
    def mock_ow_objects(self):
        mock_ambtsgebied_1 = OWAmbtsgebied(
            OW_ID="nl.imow-pv28.ambtsgebied.01",
            bestuurlijke_grenzen_verwijzing=BestuurlijkeGrenzenVerwijzing(
                bestuurlijke_grenzen_id="PV28",
                domein="NL.BI.BestuurlijkGebied",
                geldig_op="2023-09-29",
            ),
            noemer="Ambtsgebied 1",
            mapped_uuid=UUID("00000000-0000-0000-0000-000000000001"),
        )

        mock_regelingsgebied_1 = OWRegelingsgebied(
            OW_ID="nl.imow-pv28.regelingsgebied.01",
            ambtsgebied=mock_ambtsgebied_1.OW_ID,
        )

        mock_gebied_1 = OWGebied(
            OW_ID="nl.imow-pv28.gebied.01",
            noemer="Gebied 1",
            mapped_geo_code="werkingsgebied-1",
            mapped_uuid=UUID("00000000-0000-0000-0000-000000000002"),
        )
        mock_gebiedengroep_1 = OWGebiedenGroep(
            OW_ID="nl.imow-pv28.gebiedengroep.01",
            noemer="Gebiedengroep 1",
            mapped_geo_code=mock_gebied_1.mapped_geo_code,
            mapped_uuid=mock_gebied_1.mapped_uuid,
            gebieden=[mock_gebied_1.OW_ID],
        )
        mock_divisie_1 = OWDivisie(
            OW_ID="nl.imow-pv28.divisie.01",
            wid="pv28_4__content_o_1",
            mapped_policy_object_code="beleidskeuze-1",
        )
        mock_tekstdeel_1 = OWTekstdeel(
            OW_ID="nl.imow-pv28.tekstdeel.01",
            divisie=mock_divisie_1.OW_ID,
            locaties=[mock_gebiedengroep_1.OW_ID],
            gebiedsaanwijzingen=None,
        )
        mock_divisie_2 = OWDivisie(
            OW_ID="nl.imow-pv28.divisie.02",
            wid="pv28_4__content_o_2",
            mapped_policy_object_code="beleidskeuze-2",
        )
        mock_tekstdeel_2 = OWTekstdeel(
            OW_ID="nl.imow-pv28.tekstdeel.02",
            divisie=mock_divisie_2.OW_ID,
            locaties=[mock_gebiedengroep_1.OW_ID],
            gebiedsaanwijzingen=None,
        )

        return [
            mock_ambtsgebied_1,
            mock_regelingsgebied_1,
            mock_gebied_1,
            mock_gebiedengroep_1,
            mock_divisie_1,
            mock_tekstdeel_1,
            mock_divisie_2,
            mock_tekstdeel_2,
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
    def setup_method(self, mock_ow_data: OwData):
        """Setup method to initialize common resources."""

        self.context = BuilderContext(
            provincie_id="pv28",
            ow_procedure_status=None,
            levering_id="10000000-0000-0000-0000-000000000001",
            orphaned_wids=[],
        )
        self.expected_gba_wid = "pv28_4__content_o_1__ref_o_1"
        self.expected_gba_annotation = {
            "type_annotation": "gebiedsaanwijzing",
            "ref": "mock-ref-werkingsgebied-1",
            "werkingsgebied_code": "werkingsgebied-1",
            "groep": "NationaalLandschap",
            "type": "Landschap",
            "parent_div": {
                "wid": "pv28_4__content_o_2",
                "object-code": "beleidskeuze-2",
                "gebied-code": None,
                "uses_ambtsgebied": True,
            },
        }
        self.annotation_lookup_map = {
            "beleidskeuze-2": {
                "type_annotation": "ambtsgebied",
                "tag": "Divisietekst",
                "wid": "pv28_4__content_o_2",  # existing ow annotation
                "object_code": "beleidskeuze-2",  # existing policy obj code
            },
            self.expected_gba_wid: self.expected_gba_annotation,
        }
        self.ow_repository = OWStateRepository(ow_input_data=mock_ow_data)
        self.builder = OwGebiedsaanwijzingBuilder(
            context=self.context, annotation_lookup_map=self.annotation_lookup_map, ow_repository=self.ow_repository
        )

    def test_builder_init(self):
        assert self.builder._context == self.context
        assert self.builder._annotation_lookup_map == self.annotation_lookup_map
        assert self.builder._used_object_types == set()
        assert self.builder._ow_repository == self.ow_repository

    def test_handle_ow_objects(self, mock_ow_objects):
        """
        tests:
        - new gebiedsaanwijzing is created on existing div+tekstdeel without existing gba's
        TODO:
        - multiple gba
        - mutate existing tekstdeel gba
        """
        # setup
        bk2_tekstdeel = mock_ow_objects[7]
        assert bk2_tekstdeel.gebiedsaanwijzingen is None
        # expecting existing tekstdeel in mutation lane as gba origin
        self.ow_repository._mutated_ow_objects = [bk2_tekstdeel]

        # runs over the annotation lookup map set in service init
        self.builder.handle_ow_object_changes()

        assert len(self.ow_repository._new_ow_objects) == 1
        # new gba created
        new_gba = self.ow_repository._new_ow_objects[0]
        assert isinstance(new_gba, OWGebiedsaanwijzing)
        assert new_gba.locaties == ["nl.imow-pv28.gebiedengroep.01"]  # werkingsgebied-1 ref

        # mutations
        assert len(self.ow_repository._mutated_ow_objects) == 1
        mutated_state_obj_tekstdeel = self.ow_repository._mutated_ow_objects[0]
        assert isinstance(mutated_state_obj_tekstdeel, OWTekstdeel)
        assert mutated_state_obj_tekstdeel.gebiedsaanwijzingen == [new_gba.OW_ID]
