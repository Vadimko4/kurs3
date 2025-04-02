import os
from unittest import mock

import pandas as pd

from src.decorators import PATH_TO_REPORTS_XLSX_FILE, write_df_to_xlsx_file


@write_df_to_xlsx_file()
def my_foo() -> pd.DataFrame:
    df = pd.DataFrame([{'Вася': 190, 'Саша': 183}, {'Ирина': 170, 'Лена': 163}])
    return df


def test_write_df_to_xlsx_file():
    with mock.patch('pandas.DataFrame.to_excel') as mock_to_excel:
        # Вызов декорированной функции
        my_foo()

        # Проверка, что метод to_excel был вызван
        mock_to_excel.assert_called_once()

        # Проверка аргументов, с которыми был вызван метод
        args, kwargs = mock_to_excel.call_args
        assert kwargs['index'] is False  # Проверяем, что index=False
        assert args[0] == os.path.join(PATH_TO_REPORTS_XLSX_FILE, 'report.xlsx')  # Проверяем имя файла
