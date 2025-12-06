from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import get_data, spending_by_category


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    data = {
        "Дата платежа": ["2021-10-01", "2021-10-02", "2021-11-01"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"],
        "Сумма операции": [-1500, -800, -500],
    }
    df = pd.DataFrame(data)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"])
    return df


def test_spending_by_category(sample_transactions: pd.DataFrame) -> None:
    result = spending_by_category(sample_transactions, "Супермаркеты", "2021-10-15")
    assert len(result) == 2
    assert result["Категория"].iloc[0] == "Супермаркеты"


@patch("pandas.read_excel")
def test_get_data(mock_read_excel: Any, sample_transactions: pd.DataFrame) -> Any:
    mock_read_excel.return_value = sample_transactions
    get_data("test.xlsx")
    mock_read_excel.assert_called_once_with("test.xlsx", sheet_name="Отчет по операциям")
