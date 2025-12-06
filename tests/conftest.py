from typing import Any

import pytest


@pytest.fixture
def valid_datetime() -> Any:
    """Фикстура с валидной датой для тестов"""
    return "2020-05-20 12:12:12"


@pytest.fixture
def invalid_datetime() -> Any:
    """Фикстура с невалидной датой"""
    return "invalid-date"
