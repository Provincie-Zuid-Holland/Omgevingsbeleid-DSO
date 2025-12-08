from unittest.mock import MagicMock, Mock

from dso.act_builder.services.aanlevering_besluit.besluit_versie.consolidatie_informatie_content import (
    ConsolidatieInformatieContent,
)
from dso.act_builder.state_manager import ArtikelEidRepository
from dso.act_builder.state_manager.states.artikel_eid_repository import ArtikelEidData, ArtikelEidType
from dso.models import RegelingMutatie, GioFRBR
from tests.unit.dso.act_builder.state_manager.input_data.resource.document.document_repository import (
    document_repository_mock_with_two_new_documents,
)
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import (
    gebied_repository_mock_with_two_new_gebieden,
)
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import state_manager_mock
from tests.unit.dso.act_builder.state_manager.states.text_manipulator.model_factories import TextDataFactory
from tests.unit.dso.model_factories import (
    InstellingDoelFactory,
    ActFRBRFactory,
    GioFRBRFactory,
    VerwijderdGebiedFactory,
    FRBRType,
)
from tests.unit.xml_compare_test import XMLCompareTest


class TestConsolidatieInformatieContent(XMLCompareTest):
    def test_create(
        self,
        state_manager_mock,
        gebied_repository_mock_with_two_new_gebieden,
        document_repository_mock_with_two_new_documents,
    ) -> None:
        instelling_doel = InstellingDoelFactory(datum_juridisch_werkend_vanaf="2025-11-26").create()
        state_manager_mock.input_data.publication_settings.instelling_doel = instelling_doel
        state_manager_mock.input_data.publication_settings.regeling_frbr = ActFRBRFactory(Expression_Version=1).create()
        state_manager_mock.input_data.publication_settings.regeling_componentnaam = "pv28_omgevingsvisie_1"

        state_manager_mock.text_data = TextDataFactory().create()

        artikel_eid_repository: ArtikelEidRepository | Mock = MagicMock(spec=ArtikelEidRepository)
        artikel_eid_data: ArtikelEidData = ArtikelEidData(eid=f"eid-artikel-1", artikel_type=ArtikelEidType.WIJZIG)
        artikel_eid_repository.find_one_by_type.return_value = artikel_eid_data
        state_manager_mock.artikel_eid = artikel_eid_repository

        state_manager_mock.input_data.resources.gebied_repository = gebied_repository_mock_with_two_new_gebieden
        state_manager_mock.input_data.resources.document_repository = document_repository_mock_with_two_new_documents

        gio_frbr: GioFRBR = GioFRBRFactory(frbr_type=FRBRType.GEBIED, Expression_Version=3).create()
        gebied_to_be_deleted = VerwijderdGebiedFactory(id=3, frbr=gio_frbr).create()
        was_regeling_frbr = ActFRBRFactory(Expression_Version=1).create()
        regeling_mutatie = RegelingMutatie(
            was_regeling_frbr=was_regeling_frbr,
            te_verwijderden_gebieden=[gebied_to_be_deleted],
            bekend_wid_map={},
            bekend_wids=[],
        )
        state_manager_mock.input_data.regeling_mutatie = regeling_mutatie
        state_manager_mock.regeling_vrijetekst_aangeleverd = """<RegelingVrijetekst xmlns="https://standaarden.overheid.nl/stop/imop/tekst/">
    <ExtIoRef eId="cmp_I__content_o_1__list_o_1__item_o_2__ref_o_1"
        wId="gm0001_1__cmp_I__content_o_1__list_o_2__ref_o_1"
        ref="/join/id/regdata/pv28/2025/omgevingsvisie-1/nld@2025-11-25;103">
            /join/id/regdata/pv28/2025/omgevingsvisie-1/nld@2025-11-25;103
    </ExtIoRef>
</RegelingVrijetekst>"""

        consolidatie_informatie_content = ConsolidatieInformatieContent(state_manager_mock)
        actual = consolidatie_informatie_content.create()

        with open(self._get_xml_file_path(__file__), "r") as f:
            expected = f.read()
            assert actual == expected
