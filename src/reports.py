import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger("project_1")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler("project_1.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_data(path_to_file: str) -> pd.DataFrame:
    """Принимает путь к файлу XL"""
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    return df


def save_report(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения отчетов в JSON-формате:
    {"Категория": "Название", "Дата операции": [...], "Сумма операции": [...]}
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result_df = func(*args, **kwargs)
            if result_df.empty:
                logger.warning(f"Пустой DataFrame от {func.__name__}")
                return result_df
            report_data = {
                # "Категория": kwargs.get('category', f'{result_df["Категория"]}'),
                "Категория": result_df["Категория"][0],
                "Дата операции": result_df["Дата платежа"].dt.strftime("%Y-%m-%d").tolist(),
                "Сумма операции": result_df["Сумма операции"].abs().tolist(),
            }
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"report_{timestamp}.json"
            else:
                output_file = filename

            # Создаем директорию reports/
            os.makedirs("reports", exist_ok=True)
            filepath = os.path.join("reports", output_file)

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=4)

                total_sum = sum(report_data["Сумма операции"])
                logger.info(f"Отчет '{func.__name__}' сохранен: {filepath} (сумма: {total_sum:.2f} руб.)")

            except Exception as e:
                logger.error(f"Ошибка сохранения {func.__name__}: {e}")
            return result_df

        return wrapper

    return decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Вывод трат по категории за 3 месяца от даты. Возвращает DataFrame для JSON-сериализации."""
    logger.info(f"Генерация отчета трат по категории '{category}'")

    if transactions.empty:
        logger.warning("DataFrame с транзакциями пустой")
        return pd.DataFrame()

    if "Дата платежа" not in transactions.columns or "Категория" not in transactions.columns:
        logger.error("В DataFrame отсутствуют необходимые столбцы")
        return pd.DataFrame()

    transactions = transactions.copy()
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)

    if date is None:
        target_date = datetime.now()
    else:
        target_date = pd.to_datetime(date)  # dayfirst=True

    start_date = target_date - timedelta(days=90)
    logger.info(f"Период анализа: {start_date.date()} - {target_date.date()}")

    mask = (
        (transactions["Дата платежа"] >= start_date)
        & (transactions["Дата платежа"] <= target_date)
        & (transactions["Категория"] == category)
    )

    filtered = transactions[mask].copy()

    if filtered.empty:
        logger.warning(f"Нет транзакций по категории '{category}' за указанный период")
        return pd.DataFrame()

    result = filtered.groupby("Дата платежа")["Сумма операции"].sum().reset_index()
    result["Категория"] = category
    result = result.sort_values("Дата платежа")

    total_spent = abs(result["Сумма операции"].sum())
    logger.info(f"Найдено {len(result)} записей трат на сумму {total_spent: .2f} руб.")

    return result


if __name__ == "__main__":
    transaction = get_data("../data/operations.xlsx")
    sbc = spending_by_category(transaction, "Супермаркеты", "2021.10.1")
    print(sbc)
