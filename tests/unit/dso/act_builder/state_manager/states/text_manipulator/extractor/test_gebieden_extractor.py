from dso.act_builder.state_manager.states.text_manipulator.extractor.text_gio_extractor import TextGioExtractor
from dso.act_builder.state_manager.states.text_manipulator.models import TextData, TekstBijlageGio
from tests.unit.dso.act_builder.state_manager.state_manager_test_case import StateManagerTestCase, state_manager_mock


class TestTextGioExtractor(StateManagerTestCase):
    def test_extract(self, state_manager_mock):
        state_manager_mock.text_data = TextData()
        extractor = TextGioExtractor(state_manager_mock)
        xml_content = """<Root>
    <Divisietekst eId="div_o_1__div_o_1__div_o_1__content_o_1" wId="pv28_4__div_o_1__div_o_1__div_o_1__content_o_1"
        data-hint-object-code="beleidskeuze-1"
        data-hint-gio-key="gebied-1_gebied_2">
        Gebied 1
    </Divisietekst>
    <Divisietekst eId="div_o_1__div_o_1__div_o_1__content_o_2" wId="pv28_4__div_o_1__div_o_1__div_o_1__content_o_2"
        data-hint-object-code="beleidskeuze-1"
        data-hint-gio-key="gebied-3">
        Gebied 2
    </Divisietekst>
</Root>"""
        assert 0 == len(state_manager_mock.text_data.bijlage_gios)
        extractor.extract(xml_content)
        assert state_manager_mock.text_data.bijlage_gios == [
            TekstBijlageGio(
                gio_key="gebied-1_gebied_2",
                eid="div_o_1__div_o_1__div_o_1__content_o_1",
                wid="pv28_4__div_o_1__div_o_1__div_o_1__content_o_1",
                element="Divisietekst",
            ),
            TekstBijlageGio(
                gio_key="gebied-3",
                eid="div_o_1__div_o_1__div_o_1__content_o_2",
                wid="pv28_4__div_o_1__div_o_1__div_o_1__content_o_2",
                element="Divisietekst",
            ),
        ]
