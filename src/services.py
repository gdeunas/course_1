from datetime import datetime
from typing import Any

import pandas as pd


def get_path_and_period(path_to_file: str, period_date: list[str]) -> pd.DataFrame:
    """Принимает путь к файлу и срез начало месяца до даты, возращает срез из файла XL"""
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")
    filtered_df = df[(start_date <= df["Дата операции"]) & (df["Дата операции"] <= end_date)]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df


def analyze_cashback(file_path: str, year: int, month: int) -> Any:  # dict[str, int]:
    """Analyze Cashback"""
    df = pd.read_excel(file_path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_data = df[(df["Дата операции"].dt.year == year) & (df["Дата операции"].dt.month == month)]

    filtered_data = filtered_data[(filtered_data["Кэшбэк"] > 0)]

    filtered_data = filtered_data[(filtered_data["Сумма платежа"] < 0)]

    expenses_by_category = filtered_data.groupby("Категория")["Сумма платежа"].sum()
    cashback_by_category = abs(expenses_by_category) // 100
    result = cashback_by_category.to_dict()
    return result
