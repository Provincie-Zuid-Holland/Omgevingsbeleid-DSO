from pydantic import ValidationError
import pytest
from unittest.mock import MagicMock, patch

from dso.services.ow.models import OWGebiedsaanwijzing
from dso.services.ow.waardelijsten.imow_models import (
    TypeGebiedsaanwijzingValue,
    GebiedsaanwijzingGroepValue,
)

# fake IMOW values
MOCK_TYPE_1 = TypeGebiedsaanwijzingValue(
    uri="http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_1",
    term="type_term_1",
    label="Type Label 1",
)

MOCK_TYPE_2 = TypeGebiedsaanwijzingValue(
    uri="http://standaarden.omgevingswet.overheid.nl/typegebiedsaanwijzing/id/concept/type_uri_2",
    term="type_term_2",
    label="Type Label 2",
)

MOCK_GROUP_1A = GebiedsaanwijzingGroepValue(
    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1A",
    term="groep_term_1A",
    label="Groep Label 1A",
    type_gebiedsaanwijzing=MOCK_TYPE_1.uri,
)

MOCK_GROUP_1B = GebiedsaanwijzingGroepValue(
    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_1B",
    term="groep_term_1B",
    label="Groep Label 1B",
    type_gebiedsaanwijzing=MOCK_TYPE_1.uri,
)

MOCK_GROUP_2A = GebiedsaanwijzingGroepValue(
    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_2A",
    term="groep_term_2A",
    label="Groep Label 2A",
    type_gebiedsaanwijzing=MOCK_TYPE_2.uri,
)

MOCK_GROUP_2B = GebiedsaanwijzingGroepValue(
    uri="http://standaarden.omgevingswet.overheid.nl/imow/id/waardelijst/groep_uri_2B",
    term="groep_term_2B",
    label="Groep Label 2B",
    type_gebiedsaanwijzing=MOCK_TYPE_2.uri,
)

# fake registry instance
MOCK_IMOW_REPOSITORY = MagicMock()
MOCK_IMOW_REPOSITORY.get_all_type_gebiedsaanwijzingen.return_value = [MOCK_TYPE_1, MOCK_TYPE_2]
MOCK_IMOW_REPOSITORY.get_all_gebiedsaanwijzing_groepen.return_value = [
    MOCK_GROUP_1A, MOCK_GROUP_1B, MOCK_GROUP_2A, MOCK_GROUP_2B
]
MOCK_IMOW_REPOSITORY.get_type_gebiedsaanwijzing_uri.side_effect = lambda value: {
    MOCK_TYPE_1.uri: MOCK_TYPE_1.uri,
    MOCK_TYPE_2.uri: MOCK_TYPE_2.uri,
    MOCK_TYPE_1.term: MOCK_TYPE_1.uri,
    MOCK_TYPE_2.term: MOCK_TYPE_2.uri,
}.get(value, None)
MOCK_IMOW_REPOSITORY.get_groups_for_type.side_effect = lambda value: {
    MOCK_TYPE_1.uri: [MOCK_GROUP_1A, MOCK_GROUP_1B],
    MOCK_TYPE_2.uri: [MOCK_GROUP_2A, MOCK_GROUP_2B],
    MOCK_TYPE_1.term: [MOCK_GROUP_1A, MOCK_GROUP_1B],
    MOCK_TYPE_2.term: [MOCK_GROUP_2A, MOCK_GROUP_2B],
}.get(value, [])

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

@patch("dso.services.ow.models.imow_value_repository", new=MOCK_IMOW_REPOSITORY)
class TestOWGebiedsaanwijzing:
    def test_valid_instance_term_input(self, valid_data):
        obj = OWGebiedsaanwijzing(**valid_data)
        assert obj.OW_ID == "nl.imow-pv28.obj.mock"
        assert obj.naam == "Gebiedsaanwijzing Example 1"
        assert obj.type_ == MOCK_TYPE_1.uri
        assert obj.groep == MOCK_GROUP_1A.uri
        assert obj.locaties == ["loc1", "loc2"]
        assert obj.wid == "wid_123"

    def test_valid_instance_uri_input(self, valid_data):
        valid_data["type_"] = MOCK_TYPE_1.uri
        valid_data["groep"] = MOCK_GROUP_1A.uri

        obj = OWGebiedsaanwijzing(**valid_data)
        assert obj.OW_ID == "nl.imow-pv28.obj.mock"
        assert obj.naam == "Gebiedsaanwijzing Example 1"
        assert obj.type_ == MOCK_TYPE_1.uri
        assert obj.groep == MOCK_GROUP_1A.uri
        assert obj.locaties == ["loc1", "loc2"]
        assert obj.wid == "wid_123"

    def test_invalid_type(self, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["type_"] = "invalid_type"
        with pytest.raises(ValidationError):
            OWGebiedsaanwijzing(**invalid_data)

    def test_invalid_groep(self, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["groep"] = "invalid_groep"
        with pytest.raises(ValidationError):
            OWGebiedsaanwijzing(**invalid_data)

    def test_wrong_group_for_type(self, valid_data):
        invalid_data = valid_data.copy()
        invalid_data["type_"] = MOCK_TYPE_1.uri
        invalid_data["groep"] = MOCK_GROUP_2A.uri
        with pytest.raises(ValidationError):
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
