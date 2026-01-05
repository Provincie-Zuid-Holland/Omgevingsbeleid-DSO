from typing import List
from unittest.mock import Mock, MagicMock

import pytest

from dso.act_builder.state_manager.input_data.resource.gebieden.gio_repository import GioRepository
from dso.act_builder.state_manager.input_data.resource.gebieden.types import Gio
from tests.unit.dso.act_builder.state_manager.input_data.resource.gebieden.type_factories import (
    GioFactory,
)


@pytest.fixture
def gio_repository_mock_with_two_new_gebieden() -> GioRepository | Mock:
    gio_repository_mock: GioRepository | MagicMock = MagicMock(spec=GioRepository)
    gio_repository_mock.get_new.return_value = _get_gios()
    return gio_repository_mock


@pytest.fixture
def gio_repository_mock_with_two_gebieden() -> GioRepository | Mock:
    gio_repository_mock: GioRepository | MagicMock = MagicMock(spec=GioRepository)
    gio_repository_mock.all.return_value = _get_gios()
    return gio_repository_mock


def _get_gios(count: int = 2) -> List[Gio | Mock]:
    gios: List[Gio | Mock] = []
    for i in range(1, count + 1):
        base = (i - 1) * 3
        gebied_id = base + 1
        gebied = GioFactory(id=1 + base, gebied_ids={gebied_id + 2, gebied_id + 3}).create()
        gios.append(gebied)
    return gios


@pytest.fixture
def gio_repository_mock_empty() -> GioRepository | Mock:
    gio_repository_mock: GioRepository | MagicMock = MagicMock(spec=GioRepository)
    gio_repository_mock.get_new.return_value = []
    return gio_repository_mock
