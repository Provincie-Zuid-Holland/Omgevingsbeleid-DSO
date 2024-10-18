from uuid import UUID

import pytest

from dso.act_builder.services.ow.ow_builder_context import BuilderContext
from dso.act_builder.services.ow.ow_divisie import OwDivisieBuilder
from dso.act_builder.state_manager.exceptions import OWObjectStateException
from dso.act_builder.state_manager.states.ow_repository import OWStateRepository
from dso.models import OwData
from dso.services.ow import (
    BestuurlijkeGrenzenVerwijzing,
    OWAmbtsgebied,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OWRegelingsgebied,
    OWTekstdeel,
)


class TestOWDivisieBuilder:
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
            gio_ref=UUID("00000000-0000-0000-0000-000000000001"),
        )

        mock_regelingsgebied_1 = OWRegelingsgebied(
            OW_ID="nl.imow-pv28.regelingsgebied.01",
            ambtsgebied=mock_ambtsgebied_1.OW_ID,
        )

        mock_gebied_1 = OWGebied(
            OW_ID="nl.imow-pv28.gebied.01",
            noemer="Gebied 1",
            mapped_geo_code="werkingsgebied-1",
            gio_ref=UUID("00000000-0000-0000-0000-000000000002"),
        )
        mock_gebiedengroep_1 = OWGebiedenGroep(
            OW_ID="nl.imow-pv28.gebiedengroep.01",
            noemer="Gebiedengroep 1",
            mapped_geo_code=mock_gebied_1.mapped_geo_code,
            gio_ref=mock_gebied_1.gio_ref,
            gebieden=[mock_gebied_1.OW_ID],
        )
        mock_divisie_1 = OWDivisieTekst(
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
        mock_divisie_2 = OWDivisieTekst(
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
        self.new_divisie_data = {
            "wid": "pv28_4__content_o_10",
            "object_code": "beleidskeuze-10",
        }
        self.annotation_lookup_map = {
            "beleidskeuze-2": {
                "type_annotation": "ambtsgebied",
                "tag": "Divisietekst",
                "wid": "pv28_4__content_o_2",  # existing ow annotation
                "object_code": "beleidskeuze-2",  # existing policy obj code
            },
            self.new_divisie_data["object_code"]: {  # new divisie annotation existing werkingsgebied
                "type_annotation": "gebied",
                "wid": self.new_divisie_data["wid"],
                "tag": "Divisietekst",
                "object_code": self.new_divisie_data["object_code"],
                "gebied_code": "werkingsgebied-1",
                "gio_ref": "00000000-0000-0000-0000-000000000002",
            },
        }
        self.ow_repository = OWStateRepository(ow_input_data=mock_ow_data)
        self.builder = OwDivisieBuilder(self.context, self.annotation_lookup_map, self.ow_repository)

    def test_builder_init(self, mock_ow_objects):
        ambtsgebied = mock_ow_objects[0]
        assert self.builder._context == self.context
        assert self.builder._annotation_lookup == self.annotation_lookup_map
        assert self.builder._used_object_types == set()
        assert self.builder._ow_repository == self.ow_repository
        assert self.builder._ambtsgebied == ambtsgebied

    def test_handle_ow_objects_template_data(self, mock_ow_objects):
        """
        check full list of divisie actions are taken correctly.
        expecting:
            - terminated beleidskeuze-1 owdivisie and owtekstdeel
            - new owdivisie and owtekstdeel for beleidskeuze-2
            - existig beleidskeuze-2 mutated from werkingsgebied to ambtsgebied

        if any orphaned location is left after processing, it should not be tested in
        terminations as that is handled as dangling reference in ow state patcher
        """
        self.builder._context.orphaned_wids = [
            "pv28_4__content_o_1",  # mock_divisie_1
        ]

        # runs over the annotation lookup map set in service init
        self.builder.handle_ow_object_changes()

        # terminated beleidskeuse-1
        expected_terminated_objects = [
            mock_ow_objects[4],  # mock_divisie_1
            mock_ow_objects[5],  # mock_tekstdeel_1
        ]

        assert len(self.ow_repository._terminated_ow_objects) == 2
        assert self.ow_repository._terminated_ow_objects == expected_terminated_objects

        assert len(self.ow_repository._new_ow_objects) == 2

        # divisie
        state_obj_div = self.ow_repository._new_ow_objects[0]
        assert isinstance(state_obj_div, OWDivisieTekst)
        assert state_obj_div.wid == self.new_divisie_data["wid"]
        assert state_obj_div.mapped_policy_object_code == self.new_divisie_data["object_code"]

        # new tekstdeel
        state_obj_tekstdeel = self.ow_repository._new_ow_objects[1]
        assert isinstance(state_obj_tekstdeel, OWTekstdeel)
        assert state_obj_tekstdeel.divisie == state_obj_div.OW_ID
        assert state_obj_tekstdeel.locaties == [mock_ow_objects[3].OW_ID]

        # mutations
        assert len(self.ow_repository._mutated_ow_objects) == 1
        mutated_state_obj_tekstdeel = self.ow_repository._mutated_ow_objects[0]
        assert isinstance(state_obj_tekstdeel, OWTekstdeel)
        assert mutated_state_obj_tekstdeel.divisie == mock_ow_objects[6].OW_ID  # existing beleidskeuze-2
        assert mutated_state_obj_tekstdeel.locaties == [mock_ow_objects[0].OW_ID]  # mock ambtsgebied 1

    def test_terminate_removed_wids(self, mock_ow_objects):
        remove_wid_list = ["pv28_4__content_o_1"]  # mock divisietekst 1
        self.builder.terminate_removed_wids(orphaned_wids=remove_wid_list)

        expected_terminated_objects = [
            mock_ow_objects[4],  # mock_divisie_1
            mock_ow_objects[5],  # mock_tekstdeel_1
        ]

        assert self.ow_repository._terminated_ow_objects == expected_terminated_objects

    def test_process_new_divisie_gebied(self, mock_ow_objects):
        """
        expected pending ow state of 2 new objs:
            1x OWDivisietekst
            1x OWTekstdeel - ref to existing werkingsgebied
        """
        # ensure clean slate
        existing_state_location = mock_ow_objects[3]  # mock_gebiedengroep_1
        assert self.ow_repository._new_ow_objects == []

        mock_annotation = {
            "type_annotation": "gebied",
            "wid": self.new_divisie_data["wid"],
            "tag": "Divisietekst",
            "object_code": self.new_divisie_data["object_code"],  # new policy obj code
            "gebied_code": "werkingsgebied-1",  # existing gebied
            "gio_ref": (existing_state_location.Identifier),
        }

        self.builder.process_new_divisie(annotation_data=mock_annotation)

        assert len(self.ow_repository._new_ow_objects) == 2

        # new divisietekst
        new_divisie_state = self.ow_repository._new_ow_objects[0]
        assert isinstance(new_divisie_state, OWDivisieTekst)
        assert new_divisie_state.wid == self.new_divisie_data["wid"]
        assert new_divisie_state.mapped_policy_object_code == self.new_divisie_data["object_code"]

        # new tekstdeel
        new_tekstdeel_state = self.ow_repository._new_ow_objects[1]
        assert isinstance(new_tekstdeel_state, OWTekstdeel)
        assert new_tekstdeel_state.divisie == new_divisie_state.OW_ID
        assert new_tekstdeel_state.locaties == [existing_state_location.OW_ID]

    def test_process_new_divisie_unknown_gebied(self):
        assert self.ow_repository._new_ow_objects == []
        invalid_annotation = {
            "type_annotation": "gebied",
            "wid": self.new_divisie_data["wid"],
            "tag": "Divisietekst",
            "object_code": self.new_divisie_data["object_code"],
            "gebied_code": "werkingsgebied-99",  # unknown gebied
            "gio_ref": "99999999-0000-0005-0000-000000000002",
        }
        with pytest.raises(OWObjectStateException):
            self.builder.process_new_divisie(annotation_data=invalid_annotation)

    def test_process_new_divisie_ambtsgebied(self, mock_ow_objects):
        """
        test new policy object annotation, tagged to use ambtsgebied
        expected pending ow state is 2 new objs:
            1x OWDivisietekst
            1x OWTekstdeel - ref to ambtsgebied
        """
        assert self.ow_repository._new_ow_objects == []
        ambtsgebied_annotation = {
            "type_annotation": "ambtsgebied",
            "wid": self.new_divisie_data["wid"],
            "tag": "Divisietekst",
            "object_code": self.new_divisie_data["object_code"],  # new policy obj
        }
        self.builder.process_new_divisie(annotation_data=ambtsgebied_annotation)

        mock_ambtsgebied = mock_ow_objects[0]  # mock_ambtsgebied_1

        assert len(self.ow_repository._new_ow_objects) == 2

        # new divisietekst
        new_divisie_state = self.ow_repository._new_ow_objects[0]
        assert isinstance(new_divisie_state, OWDivisieTekst)
        assert new_divisie_state.wid == self.new_divisie_data["wid"]
        assert new_divisie_state.mapped_policy_object_code == self.new_divisie_data["object_code"]

        # new tekstdeel
        new_tekstdeel_state = self.ow_repository._new_ow_objects[1]
        assert isinstance(new_tekstdeel_state, OWTekstdeel)
        assert new_tekstdeel_state.divisie == new_divisie_state.OW_ID
        assert new_tekstdeel_state.locaties == [mock_ambtsgebied.OW_ID]

    def test_process_existing_divisie_mutate_to_ambtsgebied(self, mock_ow_objects):
        """test mutating existing policy object with gebied annotation to ambtsgebied"""
        assert self.ow_repository._new_ow_objects == []
        assert self.ow_repository._mutated_ow_objects == []

        mock_ambtsgebied_id: str = mock_ow_objects[0].OW_ID  # mock_ambtsgebied_1 id
        mock_divisie = mock_ow_objects[4]  # existing owdivisie id

        mutate_annotation_data = {
            "type_annotation": "ambtsgebied",
            "wid": mock_divisie.wid,
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-1",  # known policy obj
        }

        self.builder.process_existing_divisie(known_divisie=mock_divisie, annotation_data=mutate_annotation_data)

        assert len(self.ow_repository._mutated_ow_objects) == 1

        # mutated tekstdeel state
        state_obj = self.ow_repository._mutated_ow_objects[0]
        assert isinstance(state_obj, OWTekstdeel)
        assert state_obj.divisie == mock_divisie.OW_ID
        assert state_obj.locaties == [mock_ambtsgebied_id]

    def test_process_existing_divisie_mutate_to_gebied(self, mock_ow_objects):
        """
        test mutating existing policy object with ambtsgebied annotation to new gebied
        - (existng) beleidskeuze-1 -> (new) werkingsgebied-2
        """
        # create new gebied en gebiedengroep werkignsgebied-2
        new_gebied = OWGebied(
            OW_ID="nl.imow-pv28.gebied.02",
            noemer="Gebied 2",
            mapped_geo_code="werkingsgebied-2",
            gio_ref=UUID("00000000-0000-0000-0000-000000000003"),
        )
        new_gebiedengroep = OWGebiedenGroep(
            OW_ID="nl.imow-pv28.gebiedengroep.02",
            noemer="Gebiedengroep 2",
            mapped_geo_code=new_gebied.mapped_geo_code,
            gio_ref=new_gebied.gio_ref,
            gebieden=[new_gebied.OW_ID],
        )

        self.ow_repository._new_ow_objects.append(new_gebied)
        self.ow_repository._new_ow_objects.append(new_gebiedengroep)
        assert self.ow_repository._mutated_ow_objects == []

        mock_divisie = mock_ow_objects[4]  # existing owdivisie id

        mock_annotation = {
            "type_annotation": "gebied",
            "wid": mock_divisie.wid,
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-1",  # known policy obj
            "gebied_code": "werkingsgebied-2",  # existing gebied
            "gio_ref": "20000000-0000-0005-0000-000000000002",
        }

        # run
        self.builder.process_existing_divisie(known_divisie=mock_divisie, annotation_data=mock_annotation)

        # check state
        assert len(self.ow_repository._mutated_ow_objects) == 1
        state_obj = self.ow_repository._mutated_ow_objects[0]
        assert isinstance(state_obj, OWTekstdeel)
        assert state_obj.divisie == mock_divisie.OW_ID
        assert state_obj.locaties == [new_gebiedengroep.OW_ID]

    def test_process_existing_divisie_skip_mutation(self, mock_ow_objects):
        """
        test mutating of existing object policy to existing gebiedengroep:
        - beleidskeuze-1 -> werkingsgebied-1
        but existing ow object state tekstdeel already has these refs so mutation skipped
        """
        assert self.ow_repository._mutated_ow_objects == []
        mock_divisie = mock_ow_objects[4]  # existing owdivisie id
        mock_annotation = {
            "type_annotation": "gebied",
            "wid": mock_divisie.wid,
            "tag": "Divisietekst",
            "object_code": "beleidskeuze-1",  # known policy obj
            "gebied_code": "werkingsgebied-1",  # existing gebied
            "gio_ref": "20000000-0000-0005-0000-000000000002",
        }
        self.builder.process_existing_divisie(known_divisie=mock_divisie, annotation_data=mock_annotation)
        assert len(self.ow_repository._mutated_ow_objects) == 0
