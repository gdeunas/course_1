import json
from datetime import datetime
from unittest.mock import patch, mock_open, MagicMock

from src.utils import get_date_period, get_path_and_period, get_cards, get_top_transactions, \
    get_currency, get_stock_prices


import pandas as pd


def test_get_date_period():
    date_str = "2025-12-06 23:00:00"
    result = get_date_period(date_str)
    assert result[0] == "01.12.2025 00:00:01"
    assert result[1] == "06.12.2025 23:00:00"


def test_get_path_and_period(tmp_path):
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["05.12.2025 12:00:00", "07.12.2025 10:00:00"], dayfirst=True),
        "Сумма операции": [-100, 50],
    })
    file = tmp_path / "test.xlsx"
    with pd.ExcelWriter(file) as writer:
        df.to_excel(writer, sheet_name="Отчет по операциям", index=False)

    period = ["01.12.2025 00:00:01", "06.12.2025 23:59:59"]
    filtered = get_path_and_period(str(file), period)

    assert len(filtered) == 1
    assert filtered.iloc[0]["Сумма операции"] == -100


def test_get_cards():
    data = {
        "Номер карты": ["****1234", "****5678"],
        "Сумма операции": [-200, 300],
        "Кэшбэк": [2, 3],
        "Сумма операции с округлением": [-200, 300],
    }
    df = pd.DataFrame(data)
    result = get_cards(df)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == -200
    assert result[0]["cashback"] == -2


def test_get_top_transactions():
    data = {
        "Дата платежа": [datetime(2025, 12, 6), datetime(2025, 12, 5)],
        "Сумма операции": [1000, 2000],
        "Категория": ["Food", "Travel"],
        "Описание": ["Lunch", "Flight ticket"],
    }
    df = pd.DataFrame(data)
    top = get_top_transactions(df, top=1)
    assert len(top) == 1
    assert top[0]["amount"] == 2000
    assert top[0]["category"] == "Travel"
    assert top[0]["description"] == "Flight ticket"


def test_get_currency(monkeypatch):
    fake_json = json.dumps({
        "user_currencies": ["USD", "EUR"]
    })
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "conversion_rates": {
            "USD": 0.013,
            "EUR": 0.012
        }
    }

    def fake_request(method, url, data):
        return mock_response

    monkeypatch.setattr("builtins.open", mock_open(read_data=fake_json))
    monkeypatch.setattr("requests.request", fake_request)

    result = get_currency("dummy_path.json")
    assert any(c["currency"] == "USD" for c in result)
    assert any(c["currency"] == "EUR" for c in result)


def test_get_stock_prices(monkeypatch):
    fake_json = json.dumps({
        "user_stocks": ["AAPL", "GOOG"]
    })
    response_data = {
        "Global Quote": {
            "05. price": "150.25"
        }
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = response_data

    def fake_get(url):
        return mock_response

    monkeypatch.setattr("builtins.open", mock_open(read_data=fake_json))
    monkeypatch.setattr("requests.get", fake_get)

    result = get_stock_prices("dummy_path.json")
    assert any(s["stock"] == "AAPL" for s in result)
    assert any("price" in s for s in result)
