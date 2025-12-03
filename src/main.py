from src.views import get_date_period, main_info

if __name__ == "__main__":
    date_time = "2020-05-20 12:12:12"
    print(main_info(date_time))
    print(get_date_period(date_time))
