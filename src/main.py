from src.views import main_info
from src.services import analyze_cashback

if __name__ == "__main__":
    date_time = "2020-05-20 12:12:12"
    # print(main_info(date_time))

    result_services = analyze_cashback("../data/operations.xlsx", 2018, 5)
    print(result_services)
