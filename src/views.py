import json
from datetime import datetime
from typing import Any, Dict

from src.utils import get_date_period, get_path_and_period, get_time_for_greeting


def main_info(date_time: str) -> Dict[str, Any]:
    """функцию, принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS и
    возвращающую JSON-ответ
    2020-05-20 12:12:12"""

    greeting = get_time_for_greeting()
    date_period = get_date_period(date_time)

    sorted_df = get_path_and_period("../data/operations.xlsx", date_period)
    data = {"greeting": greeting}
    print("sorted_df")
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data
