import pytest
from xml.etree.ElementTree import fromstring

from dso.services.ewid.ewid_service import EWIDService


class TestEWIDService:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.ewid_service = EWIDService(
            wid_prefix="pv28_2",
            known_wid_map={},
            known_wids=[],
        )

    @pytest.fixture
    def mock_xml(self):
        xml_data = """
        <Lichaam eId="body" wId="body">
            <Divisietekst data-hint-object-code="visie_algemeen-1" data-hint-wid-code="visie_algemeen-1">
                <Kop>
                    <Opschrift>1. Inleiding</Opschrift>
                </Kop>
                <Inhoud>
                    <Tussenkop>Introductie</Tussenkop>
                    <Al>Lorem ipsum dolor sit amet, consectetur adipiscing elit. </Al>
                </Inhoud>
            </Divisietekst>
            <Divisie data-hint-wid-code="omgevingsvisie-custom-beleidsdoelen-and-beleidskeuzes-wrapper">
                <Kop>
                    <Opschrift>6. Beleidsdoelen en beleidskeuzes</Opschrift>
                </Kop>
                <Divisie data-hint-wid-code="omgevingsvisie-custom-beleidskeuze-beleidsdoel-419-wrapper">
                    <Kop>
                        <Opschrift>Lorem Ipsum divisie content</Opschrift>
                    </Kop>
                    <Divisietekst data-hint-ambtsgebied="True" data-hint-object-code="beleidskeuze-790"
                        data-hint-wid-code="beleidskeuze-790">
                        <Kop>
                            <Opschrift>Lorem Ipsum Divisietekst Kop</Opschrift>
                        </Kop>
                        <Inhoud>
                            <Tussenkop>Lorem ipsum tussenkop?</Tussenkop>
                            <Al>Voorbeeld inline GBA: 
                                <IntIoRef data-gebiedengroep="Bodembeheergebied"
                                    data-hint-locatie="werkingsgebied-10"
                                    data-hint-gebiedsaanwijzingtype="Bodem" href="#">
                                    Gebiedsnaam
                                </IntIoRef>
                            </Al>
                            <Tussenkop>Aanleiding</Tussenkop>
                            <Al>Lorem ipsum dolor sit amet.</Al>
                        </Inhoud>
                    </Divisietekst>
                </Divisie>
            </Divisie>
        </Lichaam>
        """
        return fromstring(xml_data)

    @pytest.fixture
    def additional_xml(self):
        xml_data = """
        <Divisietekst data-hint-object-code="visie_algemeen-2" data-hint-wid-code="visie_algemeen-2">
            <Kop>
                <Opschrift>2. Additional</Opschrift>
            </Kop>
            <Inhoud>
                <Tussenkop>Lipsum</Tussenkop>
                <Al>Lorem ipsum dolor sit amet, consectetur adipiscing elit. </Al>
            </Inhoud>
        </Divisietekst>
        """
        return fromstring(xml_data)

    def test_fill_ewid(self, mock_xml):
        self.ewid_service._fill_ewid(mock_xml)
        import xml.etree.ElementTree as ET

        result_xml: str = ET.tostring(mock_xml, encoding="utf-8").decode("utf-8")
        print(result_xml)

        # assert lichaam root not touched
        assert mock_xml.get("eId") == "body"
        assert mock_xml.get("wId") == "body"

        divisietekst = mock_xml.find("Divisietekst")
        assert divisietekst.get("eId") == "content_o_1"
        assert divisietekst.get("wId") == "pv28_2__content_o_1"

        # assert element not in element_ref list gets no wid
        inhoud = divisietekst.find("Inhoud")
        assert inhoud.get("eId") is None
        assert inhoud.get("wId") is None

        divisie = mock_xml.find("Divisie")
        assert divisie.get("eId") == "div_o_1"
        assert divisie.get("wId") == "pv28_2__div_o_1"

        sub_divisie = divisie.find("Divisie")
        assert sub_divisie.get("eId") == "div_o_1__div_o_1"
        assert sub_divisie.get("wId") == "pv28_2__div_o_1__div_o_1"

        sub_divisietekst = sub_divisie.find("Divisietekst")
        assert sub_divisietekst.get("eId") == "div_o_1__div_o_1__content_o_1"
        assert sub_divisietekst.get("wId") == "pv28_2__div_o_1__div_o_1__content_o_1"

        # gebiedsaanwijzingen
        int_io_refs = mock_xml.findall(".//IntIoRef")
        assert int_io_refs[0].get("eId") == "div_o_1__div_o_1__content_o_1__ref_o_1"
        assert int_io_refs[0].get("wId") == "pv28_2__div_o_1__div_o_1__content_o_1__ref_o_1"

    def test_used_wids(self, mock_xml):
        # no known wids/map provided
        self.ewid_service._wid_prefix = "pv28_2"
        self.ewid_service._fill_ewid(mock_xml)

        # ensure all new prefix
        assert self.ewid_service.get_state_used_wids() == [
            "pv28_2__content_o_1",
            "pv28_2__div_o_1",
            "pv28_2__div_o_1__div_o_1",
            "pv28_2__div_o_1__div_o_1__content_o_1",
            "pv28_2__div_o_1__div_o_1__content_o_1__ref_o_1",
        ]
        assert self.ewid_service.get_state_used_wid_map() == {
            "visie_algemeen-1": "pv28_2__content_o_1",
            "omgevingsvisie-custom-beleidsdoelen-and-beleidskeuzes-wrapper": "pv28_2__div_o_1",
            "omgevingsvisie-custom-beleidskeuze-beleidsdoel-419-wrapper": "pv28_2__div_o_1__div_o_1",
            "beleidskeuze-790": "pv28_2__div_o_1__div_o_1__content_o_1",
        }

    def test_known_wids_reused(self, mock_xml, additional_xml):
        # pv28_2 known wids/map provided
        self.ewid_service._wid_prefix = "pv28_3"
        known_wids = [
            "pv28_2__content_o_1",
            "pv28_2__div_o_1",
            "pv28_2__div_o_1__div_o_1",
            "pv28_2__div_o_1__div_o_1__content_o_1",
            "pv28_2__div_o_1__div_o_1__content_o_1__ref_o_1",
        ]
        self.ewid_service._known_wids = {wid: True for wid in known_wids}
        self.ewid_service._known_wid_map = {
            "visie_algemeen-1": "pv28_2__content_o_1",
            "omgevingsvisie-custom-beleidsdoelen-and-beleidskeuzes-wrapper": "pv28_2__div_o_1",
            "omgevingsvisie-custom-beleidskeuze-beleidsdoel-419-wrapper": "pv28_2__div_o_1__div_o_1",
            "beleidskeuze-790": "pv28_2__div_o_1__div_o_1__content_o_1",
        }

        # add another mock divisie
        mock_xml.append(additional_xml)
        self.ewid_service._fill_ewid(mock_xml)

        # ensure known wids reused and only added xml has new prefix
        assert self.ewid_service.get_state_used_wids() == [
            "pv28_2__content_o_1",
            "pv28_2__div_o_1",
            "pv28_2__div_o_1__div_o_1",
            "pv28_2__div_o_1__div_o_1__content_o_1",
            "pv28_2__div_o_1__div_o_1__content_o_1__ref_o_1",
            "pv28_3__content_o_2",
        ]

        # find added xml and ensure new prefix used
        divisietekst = mock_xml.findall("Divisietekst")[-1]
        assert divisietekst.get("eId") == "content_o_2"
        assert divisietekst.get("wId") == "pv28_3__content_o_2"

    def test_generate_eid(self):
        # Test cases for _generate_eid
        eid1 = self.ewid_service._generate_eid("Divisie", "", "")
        assert eid1 == "div_o_1"

        eid2 = self.ewid_service._generate_eid("Divisie", "body", "")
        assert eid2 == "body__div_o_1"

        eid3 = self.ewid_service._generate_eid("Divisietekst", "body__div_o_1", "")
        assert eid3 == "body__div_o_1__content_o_1"

        # Test incrementing parent counters
        eid4 = self.ewid_service._generate_eid("Divisie", "", "")
        assert eid4 == "div_o_2"

    def test_generate_wid(self):
        # Test cases for _generate_wid
        wid1 = self.ewid_service._generate_wid("Divisie", "", "")
        assert wid1 == "__div_o_1"

        wid2 = self.ewid_service._generate_wid("Divisie", "pv28_2__body", "")
        assert wid2 == "pv28_2__body__div_o_1"

        wid3 = self.ewid_service._generate_wid("Divisietekst", "pv28_2__body__div_o_1", "")
        assert wid3 == "pv28_2__body__div_o_1__content_o_1"

        # Test incrementing parent counters
        wid4 = self.ewid_service._generate_wid("Divisie", "", "")
        assert wid4 == "__div_o_2"
