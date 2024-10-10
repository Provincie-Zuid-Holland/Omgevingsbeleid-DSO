from uuid import UUID

import pytest

from dso.act_builder.services.ow.ow_builder_context import BuilderContext
from dso.act_builder.services.ow.ow_locaties import OwLocatieBuilder
from dso.act_builder.state_manager.input_data.ambtsgebied import Ambtsgebied
from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from dso.act_builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from dso.act_builder.state_manager.states.ow_repository import OWStateRepository
from dso.models import OwData
from dso.services.ow import BestuurlijkeGrenzenVerwijzing, OWAmbtsgebied, OWGebied, OWGebiedenGroep, OWRegelingsgebied


class TestOWLocatieBuilder:
    @pytest.fixture()
    def mock_location_objects(self):
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
            mapped_uuid=UUID("00000000-0000-0005-0000-000000000001"),
        )
        mock_gebiedengroep_1 = OWGebiedenGroep(
            OW_ID="nl.imow-pv28.gebiedengroep.01",
            noemer="Gebiedengroep 1",
            mapped_geo_code=mock_gebied_1.mapped_geo_code,
            mapped_uuid=mock_gebied_1.mapped_uuid,
            gebieden=[mock_gebied_1.OW_ID],
        )
        mock_gebied_2 = OWGebied(
            OW_ID="nl.imow-pv28.gebied.02",
            noemer="Gebied 2",
            mapped_geo_code="werkingsgebied-2",
            mapped_uuid=UUID("20000000-0000-0005-0000-000000000002"),
        )
        mock_gebiedengroep_2 = OWGebiedenGroep(
            OW_ID="nl.imow-pv28.gebiedengroep.02",
            noemer="Gebiedengroep 2",
            mapped_geo_code=mock_gebied_2.mapped_geo_code,
            mapped_uuid=mock_gebied_2.mapped_uuid,
            gebieden=[mock_gebied_2.OW_ID],
        )

        return [
            mock_ambtsgebied_1,
            mock_regelingsgebied_1,
            mock_gebied_1,
            mock_gebiedengroep_1,
            mock_gebied_2,
            mock_gebiedengroep_2,
        ]

    @pytest.fixture()
    def mock_ow_data(self, mock_location_objects):
        mock_ow_data = OwData(
            ow_objects={},
            terminated_ow_ids=[],
        )

        for obj in mock_location_objects:
            mock_ow_data.ow_objects[obj.OW_ID] = obj

        return mock_ow_data

    @pytest.fixture(autouse=True)
    def setup_method(self, mock_ow_data: OwData, input_data_werkingsgebieden):
        """Setup method to initialize common resources."""
        self.werkingsgebied_repo = WerkingsgebiedRepository()
        self.werkingsgebied_repo.add_from_dict(input_data_werkingsgebieden)
        self.all_input_werkingsgebieden = self.werkingsgebied_repo.all()

        self.mock_input_data_ambtsgebied: Ambtsgebied = Ambtsgebied(
            UUID=UUID("00000000-0000-0000-0000-000000000001"),
            identificatie_suffix="PV28",
            domein="NL.BI.BestuurlijkGebied",
            geldig_op="2023-09-29",
            titel="Ambtsgebied 1",
        )
        self.context = BuilderContext(
            provincie_id="pv28",
            ow_procedure_status=None,
            levering_id="10000000-0000-0000-0000-000000000001",
            orphaned_wids=[],
        )
        self.ow_repository = OWStateRepository(ow_input_data=mock_ow_data)
        self.builder = OwLocatieBuilder(
            context=self.context,
            werkingsgebieden=self.all_input_werkingsgebieden,
            ambtsgebied=self.mock_input_data_ambtsgebied,
            ow_repository=self.ow_repository,
        )

    def test_builder_init(self):
        assert self.builder._context == self.context
        assert self.builder._used_object_types == set()
        assert self.builder._ow_repository == self.ow_repository
        assert len(self.builder._werkingsgebieden) == 3
        # ensure clean repo state
        assert self.ow_repository._new_ow_objects == []
        assert self.ow_repository._mutated_ow_objects == []
        assert self.ow_repository._terminated_ow_objects == []

    def test_handle_ow_object_changes(self, enable_debugpy):
        """
        expecting:
            - input werkingsgebied-1, werkingsgebied-2 exist in ow state with same UUID: no changes
            - input_data werkingsgebied-3 not yet in ow state: new OWGebied and OWGebiedenGroep objects
        """
        input_gebied_new = self.all_input_werkingsgebieden[2]
        # existing in ow state
        input_gebied_1 = self.all_input_werkingsgebieden[0]
        input_gebied_2 = self.all_input_werkingsgebieden[1]
        # update UUID so that OWGebied needs mutation
        input_gebied_2.UUID = UUID("88888888-8888-8888-8888-888888888888")
        input_gebied_2.Locaties[0].UUID = input_gebied_2.UUID
        self.builder._werkingsgebieden[1] = input_gebied_2

        # run
        self.builder.handle_ow_object_changes()

        assert len(self.ow_repository._mutated_ow_objects) == 2 # 2 because ambtsgebied forced mutation
        assert self.ow_repository._mutated_ow_objects[1].mapped_uuid == input_gebied_2.UUID

        assert len(self.ow_repository._new_ow_objects) == 2
        assert self.ow_repository._new_ow_objects[0].mapped_uuid == input_gebied_new.UUID
        assert self.ow_repository._new_ow_objects[1].mapped_geo_code == input_gebied_new.Code

    def test_new_ow_gebiedengroep(self):
        # try input data werkingsgebied-3 - Example Geo 3 not yet in ow state
        input_data_werkingsgebied: Werkingsgebied = self.all_input_werkingsgebieden[2]

        # run
        self.builder.new_ow_gebiedengroep(werkingsgebied=input_data_werkingsgebied)

        # expect new OWGebied and OWGebiedenGroep objects
        assert len(self.ow_repository._new_ow_objects) == 2
        new_gebied = self.ow_repository._new_ow_objects[0]
        new_groep = self.ow_repository._new_ow_objects[1]
        assert isinstance(new_gebied, OWGebied)
        assert new_gebied.mapped_uuid == input_data_werkingsgebied.UUID
        assert isinstance(new_groep, OWGebiedenGroep)
        assert new_groep.mapped_geo_code == input_data_werkingsgebied.Code
        assert new_groep.gebieden == [new_gebied.OW_ID]

        assert len(self.ow_repository._mutated_ow_objects) == 0
        assert len(self.ow_repository._terminated_ow_objects) == 0
