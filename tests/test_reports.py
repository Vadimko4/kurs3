import numpy as np
import pandas as pd

from src.reports import spending_by_category


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
                'Сумма операции с округлением': 200.0
            }
        ]

    expected_df = pd.DataFrame(expected_operations)
    assert_df = spending_by_category(in_df, 'Фастфуд', '22.08.2021')
    expected_df = expected_df.reset_index(drop=True)
    assert_df = assert_df.reset_index(drop=True)
    pd.testing.assert_frame_equal(assert_df, expected_df)
