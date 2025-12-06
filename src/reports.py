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

# stream_handler = logging.StreamHandler()
# logger.addHandler(stream_handler)
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

file_handler = logging.FileHandler("project_1.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_data(path_to_file: str) -> pd.DataFrame:
    """Принимает путь к файлу XL"""
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")
    return df


# def save_report(filename: Optional[str] = None) -> Callable:
#     """Декоратор для сохранения отчетов в JSON-файл."""
#
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         def wrapper(*args: Any, **kwargs: Any) -> Any:
#             try:
#                 result = func(*args, **kwargs)
#
#                 # Определяем имя файла
#                 if filename:
#                     output_file = filename
#                 else:
#                     output_file = f"{func.__name__}_report.txt"
#
#                 # Создаем директорию reports если её нет
#                 os.makedirs("reports", exist_ok=True)
#                 output_file = os.path.join("reports", output_file)
#
#                 with open(output_file, "w", encoding="utf-8") as f:
#                     f.write(result.to_string())
#
#                 logger.info(f"Отчет сохранен: {output_file}")
#                 return result
#
#             except Exception as e:
#                 logger.error(f"Ошибка при сохранении отчета {func.__name__}: {e}")
#                 raise
#
#         return wrapper
#
#     return decorator

# old
# def save_report(filename: Optional[str] = None) -> Callable:
#     """
#     Декоратор для сохранения результатов отчетов в файл.
#
#     Без параметров: сохраняет в файл 'report_{timestamp}.json'
#     С параметром: сохраняет в указанный файл
#     """
#
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             result = func(*args, **kwargs)
#
#             if filename is None:
#                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 default_filename = f"report_{timestamp}.json"
#                 filepath = default_filename
#             else:
#                 filepath = filename
#
#             # Создаем директорию если не существует
#             os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
#
#             try:
#                 # Сохраняем в JSON
#                 with open(filepath, 'w', encoding='utf-8') as f:
#                     json.dump(result, f, ensure_ascii=False, indent=2)
#
#                 logger.info(f"Отчет сохранен в файл: {filepath}")
#
#             except Exception as e:
#                 logger.error(f"Ошибка сохранения отчета {filepath}: {e}")
#
#             return result
#
#         return wrapper
#
#     return decorator


# old
# @save_report()
# def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
#     """Вывод трат по категориям за 3 месяца от даты"""
#     logger.info(f"Генерация отчета трат по категории '{category}'")
#
#     if transactions.empty:
#         logger.warning("DataFrame с транзакциями пустой")
#         return pd.DataFrame()
#
#     # Преобразование столбца date в datetime
#     if "Дата платежа" not in transactions.columns:
#         logger.error("В DataFrame отсутствует столбец 'date'")
#         return pd.DataFrame()
#
#     transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
#
#     # Определение целевой даты
#     if date is None:
#         target_date = datetime.now()
#     else:
#         target_date = pd.to_datetime(date, dayfirst=False)
#
#     # Дата 3 месяца назад
#     start_date = target_date - timedelta(days=90)
#
#     logger.info(f"Период анализа: {start_date.date()} - {target_date.date()}")
#
#     # Фильтрация по периоду, категории и суммирование трат
#     filtered = transactions[
#         (transactions["Дата платежа"] >= start_date)
#         & (transactions["Дата платежа"] <= target_date)
#         & (transactions["Категория"] == category)
#         ]
#
#     if filtered.empty:
#         logger.warning(f"Нет транзакций по категории '{category}' за указанный период")
#         return pd.DataFrame()
#
#     result = filtered.groupby("Дата платежа")["Сумма операции"].sum().reset_index()
#     result["Категория"] = category
#
#     logger.info(f"Найдено {len(result)} записей трат на сумму {abs(result['Сумма операции'].sum()): .2f}")
#     return result


# new
# @save_report()
# def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
#     """
#     Отчет: Траты по категориям.
#     Возвращает словарь с категориями и суммами трат.
#     """
#     # Пример данных трат (в реальности загружаются из БД/файла)
#     # sample_data = [
#     #     {"date": "2025-12-01", "category": "Еда", "amount": 1500},
#     #     {"date": "2025-12-01", "category": "Транспорт", "amount": 500},
#     #     {"date": "2025-12-02", "category": "Еда", "amount": 1200},
#     #     {"date": "2025-12-02", "category": "Развлечения", "amount": 800},
#     #     {"date": "2025-12-03", "category": "Транспорт", "amount": 600},
#     # ]
#
#     df = pd.to_datetime(transactions["Дата платежа"], yearfirst=True)
#
#     # df = pd.DataFrame(transactions)
#     logger.info("Данные загружены для анализа трат")
#
#     # Определение целевой даты
#     if date is None:
#         target_date = datetime.now()
#     else:
#         target_date = pd.to_datetime(date, dayfirst=False)
#
#     # Дата 3 месяца назад
#     start_date = target_date - timedelta(days=90)
#
#     logger.info(f"Период анализа: {start_date.date()} - {target_date.date()}")
#
#     # Фильтрация по периоду, категории и суммирование трат
#     filtered = transactions[
#         (transactions["Дата платежа"] >= start_date)
#         & (transactions["Дата платежа"] <= target_date)
#         & (transactions["Категория"] == category)
#         ]
#
#     # Группировка по категориям
#     # category_totals = df.groupby('category')['amount'].sum().to_dict()
#     category_totals = df.groupby(category)['Сумма операции'].sum().to_dict()
#
#     total_expenses = df['Сумма операции'].sum()
#     report_data = {
#         "period": {
#             "start": df['date'].min(),
#             "end": df['date'].max()
#         },
#         "total_expenses": float(total_expenses),
#         "expenses_by_category": {k: float(v) for k, v in category_totals.items()},
#         "generated_at": datetime.now().isoformat()
#     }
#
#     logger.info(f"Отчет сформирован. Общие траты: {total_expenses} руб.")
#     return report_data

# new2
# def save_report(filename: Optional[str] = None) -> Callable:
#     """
#     Декоратор для сохранения результатов отчетов в JSON-файл.
#     Без параметров: сохраняет в 'report_YYYYMMDD_HHMMSS.json'
#     С параметром: сохраняет в указанный файл
#     """
#
#     def decorator(func: Callable) -> Callable:
#         @wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             result = func(*args, **kwargs)
#             if filename is None:
#                 timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#                 output_file = f"report_{timestamp}.json"
#             else:
#                 output_file = filename
#
#             # Создаем директорию reports/
#             os.makedirs("reports", exist_ok=True)
#             filepath = os.path.join("reports", output_file)
#
#             try:
#                 # Сохраняем в JSON (автоматически обрабатывает DataFrame/list/dict)
#                 with open(filepath, 'w', encoding='utf-8') as f:
#                     json.dump(result, f, ensure_ascii=False, indent=4, default=str)
#
#                 logger.info(f"Отчет '{func.__name__}' сохранен: {filepath}")
#
#             except Exception as e:
#                 logger.error(f"Ошибка сохранения {func.__name__}: {e}")
#             return result
#
#         return wrapper
#
#     return decorator


# news3
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


# new2
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
