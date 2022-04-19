from datetime import date, datetime, timedelta
from lib2to3.pytree import convert


def main():
    return 0

def holiday_detector(input_date: str) -> int:
    converted_date = None
    # try format
    try:
        converted_date = datetime.strptime(input_date, "%Y-%m-%d")
    except Exception as err:
        raise Exception("The date format is not correct, the expected form is like 1970-01-01.")

    state_holidays = ["2022-05-01", "2022-04-18", "2022-09-01"]
    range_to_holiday = []
    for holiday in state_holidays:
        converted_holiday = datetime.strptime(holiday, "%Y-%m-%d")
        difference_in_s = converted_holiday - converted_date
        diff_in_days = difference_in_s.days
        if diff_in_days > 0:
            range_to_holiday.append(abs(int(diff_in_days)))

    return f'The nearest state holiday will be in {min(range_to_holiday)} days.'

if __name__ == "__main__":
    input_date = input("Please input date string in the following format: 1970-01-01: ")
    result = holiday_detector(input_date)
    print(result)