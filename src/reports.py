import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Optional
from venv import logger

import pandas as pd


def get_data(path_to_file: str) -> pd.DataFrame:
    """Принимает путь к файлу XL"""
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    # df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    data = df
    return data


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Вывод трат по категориям за 3 месяца от даты"""
    logger.info(f"Генерация отчета трат по категории '{category}'")

    if transactions.empty:
        # logger.warning("DataFrame с транзакциями пустой")
        return pd.DataFrame()

    # Преобразование столбца date в datetime
    if "Дата платежа" not in transactions.columns:
        # logger.error("В DataFrame отсутствует столбец 'date'")
        return pd.DataFrame()

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)

    # Определение целевой даты
    if date is None:
        target_date = datetime.now()
    else:
        target_date = pd.to_datetime(date, dayfirst=True)

    # Дата 3 месяца назад
    start_date = target_date - timedelta(days=90)

    # logger.info(f"Период анализа: {start_date.date()} - {target_date.date()}")

    # Фильтрация по периоду, категории и суммирование трат
    filtered = transactions[
        (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] <= target_date)
        & (transactions["Категория"] == category)
    ]

    if filtered.empty:
        # logger.warning(f"Нет транзакций по категории '{category}' за указанный период")
        return pd.DataFrame()

    result = filtered.groupby("Дата платежа")["Сумма операции"].sum().reset_index()
    result["Категория"] = category

    # logger.info(f"Найдено {len(result)} записей трат на сумму {result['Сумма операции'].sum():.2f}")
    return result


if __name__ == "__main__":
    transaction = get_data("../data/operations.xlsx")
    sbc = spending_by_category(transaction, "Супермаркеты", "1.10.2021")
    print(sbc)
