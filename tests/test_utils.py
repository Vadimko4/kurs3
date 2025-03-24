from unittest.mock import mock_open, patch

import pytest
import datetime
import numpy as np

from src.utils import (get_greeting, get_operations_from_xlsx, PATH_TO_OPERATIONS_XLSX_FILE, filter_by_state,
                       get_date_obj_from_str_date, filter_by_date, filter_by_card, get_card_total_rub_spent,
                       get_card_cashback_rub, PATH_TO_USER_SETTINGS_JSON_FILE, get_currency_list_from_json,
                       get_stock_list_from_json)


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
    mock_get@patch('pandas.read_excel')


@patch('builtins.open', new_callable=mock_open, read_data='[]')
@patch('json.load')
def test_get_currency_list_from_json(mock_json_load, mock_open):
    mock_json_load.return_value = []

    result = get_currency_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)

    assert result == []
    mock_open.assert_called_once_with(PATH_TO_USER_SETTINGS_JSON_FILE, encoding='utf-8')
    mock_json_load.assert_called_once()


@patch('builtins.open', new_callable=mock_open, read_data='[]')
@patch('json.load')
def test_get_stock_list_from_json(mock_json_load, mock_open):
    mock_json_load.return_value = []

    result = get_stock_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)

    assert result == []
    mock_open.assert_called_once_with(PATH_TO_USER_SETTINGS_JSON_FILE, encoding='utf-8')
    mock_json_load.assert_called_once()


def test_filter_by_state(test_operation_list):
    assert filter_by_state(test_operation_list[:2]) == \
           [
               {
                   'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
                   'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -250.0,
                   'Валюта операции': 'RUB', 'Сумма платежа': -250.0,
                   'Валюта платежа': 'RUB', 'Кэшбэк': 99.0, 'Категория': 'Связь',
                   'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
                   'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
               },
               {
                   'Дата операции': '26.07.2021 18:55:26', 'Дата платежа': '26.07.2021',
                   'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -135.0,
                   'Валюта операции': 'TRY', 'Сумма платежа': -135.0, 'Валюта платежа': 'TRY',
                   'Кэшбэк': 55.0, 'Категория': 'Фастфуд', 'MCC': 5814.0, 'Описание': 'Pingvin Kofe I Chaj',
                   'Бонусы (включая кэшбэк)': 2, 'Округление на инвесткопилку': 0,
                   'Сумма операции с округлением': 135.0
               }
           ]

    assert (filter_by_state(test_operation_list, 'FAILED') ==
            [
                {
                    'Дата операции': '22.07.2021 23:53:25', 'Дата платежа': np.nan, 'Номер карты': np.nan,
                    'Статус': 'FAILED',
                    'Сумма операции': -90000.0, 'Валюта операции': 'RUB', 'Сумма платежа': -90000.0,
                    'Валюта платежа': 'RUB',
                    'Кэшбэк': np.nan, 'Категория': 'Переводы', 'MCC': np.nan, 'Описание': 'Перевод с карты',
                    'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                    'Сумма операции с округлением': 90000.0
                }
            ])


@pytest.mark.parametrize('wrong_state', ['CANCELED', 'EXECUTED', ' '])
def test_filter_by_wrong_state(wrong_state, test_operation_list):
    with pytest.raises(ValueError):
        filter_by_state(test_operation_list, wrong_state)


def test_get_date_obj_from_str_date():
    expected_date = datetime.datetime(2021, 7, 26, 20, 35, 57)
    assert get_date_obj_from_str_date('26.07.2021 20:35:57') == expected_date


@pytest.mark.parametrize('start_data, end_data, expected', [
    ('26.07.2021',
     '27.07.2021',
     [
        {
            'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
            'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -250.0,
            'Валюта операции': 'RUB', 'Сумма платежа': -250.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': 99.0, 'Категория': 'Связь',
            'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
        },
        {
            'Дата операции': '26.07.2021 18:55:26', 'Дата платежа': '26.07.2021',
            'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -135.0,
            'Валюта операции': 'TRY', 'Сумма платежа': -135.0, 'Валюта платежа': 'TRY',
            'Кэшбэк': 55.0, 'Категория': 'Фастфуд', 'MCC': 5814.0, 'Описание': 'Pingvin Kofe I Chaj',
            'Бонусы (включая кэшбэк)': 2, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 135.0
        }
     ]
     ),
    ('25.07.2021 00:00:00',
     '26.07.2021 19:00:00',
     [
        {
            'Дата операции': '26.07.2021 18:55:26', 'Дата платежа': '26.07.2021',
            'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -135.0,
            'Валюта операции': 'TRY', 'Сумма платежа': -135.0, 'Валюта платежа': 'TRY',
            'Кэшбэк': 55.0, 'Категория': 'Фастфуд', 'MCC': 5814.0, 'Описание': 'Pingvin Kofe I Chaj',
            'Бонусы (включая кэшбэк)': 2, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 135.0
        },
        {
            'Дата операции': '25.07.2021 20:55:58', 'Дата платежа': '26.07.2021',
            'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -43.0,
            'Валюта операции': 'RUB', 'Сумма платежа': -43.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Транспорт',
            'MCC': 4111.0,  'Описание': 'Северо-Западная пригородная пассажирская компания',
            'Бонусы (включая кэшбэк)': 0,  'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 43.0
        }
     ]
     ),
    ('25.07.2025',
     '26.07.2025',
     []
     )])
def test_filter_by_date(test_operation_list, start_data, end_data, expected):
    assert filter_by_date(test_operation_list, start_data, end_data) == expected


@pytest.mark.parametrize('card_number, expected', [
    (
        '*4556',
        [
        {
            'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
            'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -250.0,
            'Валюта операции': 'RUB', 'Сумма платежа': -250.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': 99.00, 'Категория': 'Связь',
            'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
        },
        {
            'Дата операции': '23.07.2021 19:00:53', 'Дата платежа': '23.07.2021',
            'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': 15000.0,
            'Валюта операции': 'RUB', 'Сумма платежа': 15000.0, 'Валюта платежа': 'RUB',
            'Кэшбэк': np.nan, 'Категория': 'Пополнения', 'MCC': np.nan,
            'Описание': 'Внесение наличных через банкомат Тинькофф',
            'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 15000.0
        }
        ]
    ),
    ('*9999', [])
])
def test_filter_by_card(test_operation_list, card_number, expected):
    assert filter_by_card(test_operation_list, card_number) == expected



def test_get_card_total_rub_spent(test_operation_list):
    assert get_card_total_rub_spent(test_operation_list[4: 6]) == 20300.00
    assert get_card_total_rub_spent(test_operation_list[0:1]) == -250.00
    assert get_card_total_rub_spent([]) == 0.00


def test_get_card_cashback_rub(test_operation_list):
    assert get_card_cashback_rub(test_operation_list[:2]) == 154.00
    assert get_card_cashback_rub(test_operation_list) == 154.00
    assert get_card_cashback_rub(test_operation_list[2:]) == 0.00
    assert get_card_cashback_rub([]) == 0.00
    assert get_card_cashback_rub([{}, {}]) == 0.00
