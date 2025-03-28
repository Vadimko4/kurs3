import numpy as np
import pandas as pd
import pytest

from src.reports import spending_by_category

#
# @pytest.mark.parametrize('date, expected', [('20.07.2025', '20.04.2025'),
#                                             ('04.04.2023', '04.01.2023'),
#                                             ('15.02.2024', '15.11.2023'),
#                                             ('31.12.2021', '30.09.2021')])
# def test_get_date_three_month_earlier(date, expected):
#     assert get_date_three_month_earlier(date) == expected


def test_spending_by_category(test_rub_operation_list):
    in_df = pd.DataFrame(test_rub_operation_list)
    expected_operations = \
        [
            {
                'Дата операции': '23.07.2021 16:05:51', 'Дата платежа': '23.07.2021', 'Номер карты': '*7197',
                'Статус': 'OK', 'Сумма операции': -40.0, 'Валюта операции': 'RUB', 'Сумма платежа': -40.0,
                'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Фастфуд', 'MCC': 5814.0,
                'Описание': 'Pyshechnaya Pyshlandiya', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 40.0
            },
            {
                'Дата операции': '23.07.2021 16:01:01', 'Дата платежа': '23.07.2021', 'Номер карты': '*7197',
                'Статус': 'OK', 'Сумма операции': -200.0, 'Валюта операции': 'RUB', 'Сумма платежа': -200.0,
                'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Фастфуд', 'MCC': 5814.0,
                'Описание': 'Pyshechnaya Pyshlandiya', 'Бонусы (включая кэшбэк)': 4, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 200.0}]
    expected_df = pd.DataFrame(expected_operations)
    pd.testing.assert_frame_equal(spending_by_category(in_df, 'Фастфуд', '22.08.2021'), expected_df)
