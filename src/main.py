import pandas as pd

from src.reports import spending_by_category
from src.services import analyze_cashback
from src.views import main_info

if __name__ == "__main__":
    date_time = "2020-05-20 12:12:12"
    # print(main_info(date_time))

    result_services = analyze_cashback("../data/operations.xlsx", 2018, 5)
    print(result_services)

    df = pd.read_excel("../data/operations.xlsx", sheet_name="Отчет по операциям")
    result_report = spending_by_category(df, "Ж/д билеты", "2020-05-20")
    print(result_report)
