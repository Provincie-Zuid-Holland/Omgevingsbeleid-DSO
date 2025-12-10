from dso.act_builder.state_manager.states.text_manipulator.extractor.gebieden_extractor import TextGebiedenExtractor
from dso.act_builder.state_manager.states.text_manipulator.models import TextData, TekstBijlageGebied
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import StateManagerTestCase, state_manager_mock


class TestTextGebiedenExtractor(StateManagerTestCase):
    def test_extract(self, state_manager_mock):
        state_manager_mock.text_data = TextData()
        extractor = TextGebiedenExtractor(state_manager_mock)
        xml_content = """<Root>
    <Divisietekst eId="div_o_1__div_o_1__div_o_1__content_o_1" wId="pv28_4__div_o_1__div_o_1__div_o_1__content_o_1"
        data-hint-object-code="beleidskeuze-1"
        data-hint-gebied-code="gebied-1">
        Gebied 1
    </Divisietekst>
    <Divisietekst eId="div_o_1__div_o_1__div_o_1__content_o_2" wId="pv28_4__div_o_1__div_o_1__div_o_1__content_o_2"
        data-hint-object-code="beleidskeuze-1"
        data-hint-gebied-code="gebied-2">
        Gebied 2
    </Divisietekst>
</Root>"""
        assert 0 == len(state_manager_mock.text_data.bijlage_gebieden)
        extractor.extract(xml_content)
        assert state_manager_mock.text_data.bijlage_gebieden == [
            TekstBijlageGebied(
                gebied_code="gebied-1",
                eid="div_o_1__div_o_1__div_o_1__content_o_1",
                wid="pv28_4__div_o_1__div_o_1__div_o_1__content_o_1",
                element="Divisietekst"
            ),
            TekstBijlageGebied(
                gebied_code="gebied-2",
                eid="div_o_1__div_o_1__div_o_1__content_o_2",
                wid="pv28_4__div_o_1__div_o_1__div_o_1__content_o_2",
                element="Divisietekst"
            ),
        ]
