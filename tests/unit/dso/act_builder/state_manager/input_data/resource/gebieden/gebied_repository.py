from typing import List
from unittest.mock import Mock, MagicMock

import pytest

from dso.act_builder.state_manager.input_data.resource.gebieden.gebied_repository import GebiedRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gebied
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.type_factories import GebiedFactory
from tests.unit.dso.model_factories import GioFRBRFactory, FRBRType


@pytest.fixture
def gebied_repository_mock_with_two_new_gebieden() -> GebiedRepository | Mock:
    gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
    gebied_repository_mock.get_new.return_value = _get_gebieden()
    return gebied_repository_mock


@pytest.fixture
def gebied_repository_mock_with_two_gebieden() -> GebiedRepository | Mock:
    gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
    gebied_repository_mock.all.return_value = _get_gebieden()
    return gebied_repository_mock


def _get_gebieden(count: int = 2) -> List[Gebied | Mock]:
    gebieden: List[Gebied | Mock] = []
    for i in range(1, count + 1):
        frbr = GioFRBRFactory(frbr_type=FRBRType.GEBIED, Expression_Version=i).create()
        gebied = GebiedFactory(id=i, frbr=frbr).create()
        gebieden.append(gebied)
    return gebieden


@pytest.fixture
def gebied_repository_mock_empty() -> GebiedRepository | Mock:
    gebied_repository_mock: GebiedRepository | MagicMock = MagicMock(spec=GebiedRepository)
    gebied_repository_mock.get_new.return_value = []
    return gebied_repository_mock
