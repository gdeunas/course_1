import json

from src.utils import (
    get_cards,
    get_currency,
    get_date_period,
    get_path_and_period,
    get_stock_prices,
    get_time_for_greeting,
    get_top_transactions,
)


def main_info(date_time: str) -> str:
    """функцию, принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS и
    возвращающую JSON-ответ
    2020-05-20 12:12:12"""
    # Фильтр данных XL
    date_period = get_date_period(date_time)
    sorted_df = get_path_and_period("../data/operations.xlsx", date_period)

    # 1. Приветствие
    greeting = get_time_for_greeting()

    # 2. По каждой карте
    cards = get_cards(sorted_df)

    # 3. Топ-5 транзакции по сумме платежа
    top_transactions = get_top_transactions(sorted_df, 5)

    # 4. Курс валют
    # currency_rates
    currencies_rates = get_currency("../user_settings.json")

    # 5. S&P500 stock prices
    stock_prices = get_stock_prices("../user_settings.json")

    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currencies_rates,
        "stock_prices": stock_prices,
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data
