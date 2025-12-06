import pytest
import pandas as pd
from src.reports import get_data, spending_by_category
from unittest.mock import patch


@pytest.fixture
def sample_transactions():
    data = {
        "Дата платежа": ["2021-10-01", "2021-10-02", "2021-11-01"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Транспорт"],
        "Сумма операции": [-1500, -800, -500]
    }
    df = pd.DataFrame(data)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"])
    return df


def test_spending_by_category(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты", "2021-10-15")
    assert len(result) == 2
    assert result["Категория"].iloc[0] == "Супермаркеты"


@patch('pandas.read_excel')
def test_get_data(mock_read_excel, sample_transactions):
    mock_read_excel.return_value = sample_transactions
    result = get_data("test.xlsx")
    mock_read_excel.assert_called_once_with("test.xlsx", sheet_name="Отчет по операциям")
