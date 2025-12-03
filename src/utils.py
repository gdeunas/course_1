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
    return df
