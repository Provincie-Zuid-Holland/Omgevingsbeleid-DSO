from pydantic import ValidationError
import pytest
from unittest.mock import MagicMock, patch

from dso.services.ow.models import OWGebiedsaanwijzing

TYPE_GEBIEDSAANWIJZING_VALUES = MagicMock()
TYPE_GEBIEDSAANWIJZING_VALUES.waarden.waarde = [
    MagicMock(
        uri="http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1",
        term="type_term_1",
        label="Type Label 1",
    ),
    MagicMock(
        uri="http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_2",
        term="type_term_2",
        label="Type Label 2",
    ),
]

GEBIEDSAANWIJZING_TO_GROEP_MAPPING = {
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1": MagicMock(
        waarden=MagicMock(
            waarde=[
                MagicMock(
                    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1A",
                    term="groep_term_1A",
                    label="Groep Label 1A",
                ),
                MagicMock(
                    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1B",
                    term="groep_term_1B",
                    label="Groep Label 1B",
                ),
            ]
        )
    ),
    "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_2": MagicMock(
        waarden=MagicMock(
            waarde=[
                MagicMock(
                    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_2A",
                    term="groep_term_2A",
                    label="Groep Label 2A",
                ),
                MagicMock(
                    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_2B",
                    term="groep_term_2B",
                    label="Groep Label 2B",
                ),
            ]
        )
    )
}

@pytest.fixture
def valid_data():
    return {
        "OW_ID": "nl.imow-pv28.obj.mock",
        "naam": "Gebiedsaanwijzing Example 1",
        "type_": "type_term_1",
        "groep": "groep_term_1A",
        "locaties": ["loc1", "loc2"],
        "wid": "wid_123",
    }

@patch("dso.services.ow.models.TYPE_GEBIEDSAANWIJZING_VALUES", new=TYPE_GEBIEDSAANWIJZING_VALUES)
@patch("dso.services.ow.models.GEBIEDSAANWIJZING_TO_GROEP_MAPPING", new=GEBIEDSAANWIJZING_TO_GROEP_MAPPING)
class TestOWGebiedsaanwijzing:
    def test_valid_instance_term_input(self, valid_data):
        obj = OWGebiedsaanwijzing(**valid_data)
        assert obj.OW_ID == "nl.imow-pv28.obj.mock"
        assert obj.naam == "Gebiedsaanwijzing Example 1"
        assert obj.type_ == "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1"
        assert obj.groep == "http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1A"
        assert obj.locaties == ["loc1", "loc2"]
        assert obj.wid == "wid_123"

    def test_valid_instance_uri_input(self, valid_data):
        valid_data["type_"] = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1"
        valid_data["groep"] = "http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1A"

        obj = OWGebiedsaanwijzing(**valid_data)
        assert obj.OW_ID == "nl.imow-pv28.obj.mock"
        assert obj.naam == "Gebiedsaanwijzing Example 1"
        assert obj.type_ == "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1"
        assert obj.groep == "http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1A"
        assert obj.locaties == ["loc1", "loc2"]
        assert obj.wid == "wid_123"

    def test_invalid_type(self, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["type_"] = "invalid_type"
        with pytest.raises(ValidationError) as exc_info:
            OWGebiedsaanwijzing(**invalid_data)

    def test_invalid_groep(self, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["groep"] = "invalid_groep"
        with pytest.raises(ValidationError) as exc_info:
            OWGebiedsaanwijzing(**invalid_data)

    def test_wrong_group_for_type(self, valid_data):
        """ valid group and valid type but type mapping does not contain this group """
        invalid_data = valid_data.copy()
        invalid_data["type_"] = "http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1"
        invalid_data["groep"] = "http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_2A"
        with pytest.raises(ValidationError) as exc_info:
            OWGebiedsaanwijzing(**invalid_data)

    def test_has_valid_refs_true(self, valid_data):
        obj = OWGebiedsaanwijzing(**valid_data)
        used_ow_ids = ["nl.imow-pv28.obj.mock", "loc1", "loc2"]
        reverse_ref_index = {"OWTekstdeel": {"nl.imow-pv28.obj.mock"}}
        assert obj.has_valid_refs(used_ow_ids, reverse_ref_index) is True

    def test_has_valid_refs_missing_locatie(self, valid_data):
        obj = OWGebiedsaanwijzing(**valid_data)
        used_ow_ids = ["nl.imow-pv28.obj.mock", "loc1"]
        reverse_ref_index = {"OWTekstdeel": {"nl.imow-pv28.obj.mock"}}
        assert obj.has_valid_refs(used_ow_ids, reverse_ref_index) is False

    def test_has_valid_refs_missing_reverse_ref(self, valid_data):
        obj = OWGebiedsaanwijzing(**valid_data)
        used_ow_ids = ["nl.imow-pv28.obj.mock", "loc1", "loc2"]
        reverse_ref_index = {"OWTekstdeel": {"other"}}
        assert obj.has_valid_refs(used_ow_ids, reverse_ref_index) is False
