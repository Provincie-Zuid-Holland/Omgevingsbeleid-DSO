from unittest.mock import MagicMock, Mock

import pytest

from dso.act_builder.state_manager import ArtikelEidRepository
from dso.act_builder.state_manager.states.artikel_eid_repository import ArtikelEidData, ArtikelEidType


@pytest.fixture
def artikel_eid_repository_with_eid_data() -> ArtikelEidRepository | Mock:
    artikel_eid_repository_mock: ArtikelEidRepository | MagicMock = MagicMock(spec=ArtikelEidRepository)
    artikel_eid_data: ArtikelEidData = ArtikelEidData(eid="eid-artikel-1", artikel_type=ArtikelEidType.WIJZIG)
    artikel_eid_repository_mock.find_one_by_type.return_value = artikel_eid_data
    return artikel_eid_repository_mock
