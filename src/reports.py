from typing import Optional

import datetime
import pandas as pd


def get_date_three_month_earlier(target_date: str) -> str:
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    day = target_date[:2]
    month = target_date[3:5]
    year = target_date[-4:]

    new_day = day
    new_month = months[int(month) - 4]
    if int(month) < 4:
        new_year = str(int(year) - 1)
    else:
        new_year = year
    new_date = f'{new_day}.{new_month}.{new_year}'
    return new_date


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date_obj = datetime.datetime.now()
        date = date_obj.strftime("%d.%m.%Y")

    start_date_operations = f"{get_date_three_month_earlier(date)} 00:00:00"
    end_date_operations = f"{date} 23:59:59"
    pass