from datetime import datetime

import pandas as pd
from pandas import DataFrame


def get_time_for_greeting() -> str:
    """Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени."""

    users_datetime_hour = datetime.now().hour
    greeting_list = ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]
    if 5 <= users_datetime_hour < 12:
        return greeting_list[0]
    elif 12 <= users_datetime_hour < 18:
        return greeting_list[1]
    elif 18 <= users_datetime_hour < 22:
        return greeting_list[2]
    else:
        return greeting_list[3]


def get_date_period(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    """Возаращает словарь [первого дня месяца] и [дату месяца] формата '%Y-%m-%d %H:%M:%S"""
    dt = datetime.strptime(date_time, date_format)
    first_date = dt.replace(day=1)
    return [first_date.strftime("%d.%m.%Y 00:00:01"), dt.strftime("%d.%m.%Y %H:%M:%S")]


def get_path_and_period(path_to_file: str, period_date: list[str]) -> DataFrame:
    """Принимает путь к файлу и срез начало месяца до даты, возращает срез из файла XL"""
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")
    filtered_df = df[(start_date <= df["Дата операции"]) & (df["Дата операции"] <= end_date)]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    # print(sorted_df)
    return sorted_df


def get_cards(sorted_df: DataFrame) -> list[dict]:
    """Вывод данных карт {ХХХХ...}"""
    cards_transactions = []
    cards_sorted = sorted_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк",
            "Сумма операции с округлением",
        ]
    ]
    for index, row in cards_sorted.iterrows():
        # print(index, row)
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            # cashback = row['Кэшбэк']
            cashback = total_spent // 100
            row = {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback,
            }

            cards_transactions.append(row)
    return cards_transactions


def get_top_transactions(sorted_df: DataFrame, top: int) -> list[dict]:
    """Топ 5 транзакции по сумме платежа"""
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(top)

    top_pay_transactions_sorted = top_transactions[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание",
        ]
    ]
    for index, row in top_pay_transactions_sorted.iterrows():
        # print(row)
        top_date = row["Дата платежа"]
        top_amount = row["Сумма операции"]
        top_category = row["Категория"]
        top_description = row["Описание"]
        transaction = {
            "date": top_date,
            "amount": top_amount,
            "category": top_category,
            "description": top_description,
        }
        top_pay_transactions.append(transaction)
    return top_pay_transactions


def get_currency() -> str:
    """Курс вавлюты"""
    return ""
