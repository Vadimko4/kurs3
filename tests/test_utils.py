from unittest.mock import patch
from src.utils import (get_greeting, get_operations_from_xlsx,
                       PATH_TO_OPERATIONS_XLSX_FILE, filter_by_state)


@patch("src.utils.datetime.datetime")
def test_get_greeting(mock_datetime):
    mock_datetime.now.return_value.hour = 10
    assert get_greeting() == "Доброе утро!"
    mock_datetime.now.return_value.hour = 15
    assert get_greeting() == "Добрый день!"
    mock_datetime.now.return_value.hour = 20
    assert get_greeting() == "Добрый вечер!"
    mock_datetime.now.return_value.hour = 1
    assert get_greeting() == "Доброй ночи!"


@patch('pandas.read_excel')
def test_get_operations_from_xlsx(mock_get):
    mock_get.return_value.to_dict.return_value = []
    assert get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE) == []
    mock_get.assert_called_with(PATH_TO_OPERATIONS_XLSX_FILE)


def test_filter_by_state(test_operation_list) -> None:
    assert filter_by_state(test_operation_list[:2]) == \
           [
               {
                   'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
                   'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -250.0,
                   'Валюта операции': 'RUB', 'Сумма платежа': -250.0,
                   'Валюта платежа': 'RUB', 'Кэшбэк': None, 'Категория': 'Связь',
                   'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
                   'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
               },
               {
                   'Дата операции': '26.07.2021 18:55:26', 'Дата платежа': '26.07.2021',
                   'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -135.0,
                   'Валюта операции': 'RUB', 'Сумма платежа': -135.0, 'Валюта платежа': 'RUB',
                   'Кэшбэк': None, 'Категория': 'Фастфуд', 'MCC': 5814.0, 'Описание': 'Pingvin Kofe I Chaj',
                   'Бонусы (включая кэшбэк)': 2, 'Округление на инвесткопилку': 0,
                   'Сумма операции с округлением': 135.0
               }
           ]

    assert (filter_by_state(test_operation_list, 'FAILED') ==
            [
                {
                    'Дата операции': '22.07.2021 23:53:25', 'Дата платежа': None, 'Номер карты': None,
                    'Статус': 'FAILED',
                    'Сумма операции': -90000.0, 'Валюта операции': 'RUB', 'Сумма платежа': -90000.0,
                    'Валюта платежа': 'RUB',
                    'Кэшбэк': None, 'Категория': 'Переводы', 'MCC': None, 'Описание': 'Перевод с карты',
                    'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                    'Сумма операции с округлением': 90000.0
                }
            ])
