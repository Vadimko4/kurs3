from unittest.mock import patch

import pytest

from src.external_api import get_rub_transaction_amount, get_currency_too_rub_rate, get_stock_rub_price, stocks_api_key


@patch('requests.get')
def test_get_rub_transaction_amount(mock_get, test_operation_list):
    mock_get.return_value.json.return_value = {'result': 10000.00}
    assert get_rub_transaction_amount(test_operation_list[1]) == -10000.00
    mock_get.assert_called_once()

    assert get_rub_transaction_amount(test_operation_list[0]) == -250.00


@pytest.mark.parametrize('wrong_transaction', [{}, {"Сумма операции": -250.0}, {"Валюта операции": "USD"}])
def test_get_rub_wrong_transaction_amount(wrong_transaction):
    with pytest.raises(ValueError):
        get_rub_transaction_amount(wrong_transaction)


@patch('requests.get')
def test_get_currency_too_rub_rate(mock_get):
    mock_get.return_value.json.return_value = {'info': {"rate": 1000.00}}
    assert get_currency_too_rub_rate('USD') == 1000.00
    mock_get.assert_called_once()


#  как тестировать функцию, которая содержит сначала обращение к api,
#  а потом вызов другой функции, которая тоже внутри себя содержит ещё одно
#  обращение  - к другой api
@patch('requests.get')
@patch('src.external_api.get_rub_transaction_amount')
def test_get_stock_rub_price(mock_get_rub_transaction_amount, mock_get_stock_price):
    mock_get_stock_price.return_value.json.return_value = {'data': [{"open": 100.00}]}
    mock_get_rub_transaction_amount.return_value = 10000.00
    # Вызываем тестируемую функцию
    rub_amount = get_stock_rub_price('TSLA')

    # Проверяем, что функция возвращает ожидаемое значение
    assert rub_amount == 10000.00

    # Проверяем, что оба API были вызваны
    expected_url = f"https://api.marketstack.com/v1/eod?access_key={stocks_api_key}"
    expected_params = {"symbols": 'TSLA'}
    mock_get_stock_price.assert_called_once_with(expected_url, params=expected_params)
    mock_get_rub_transaction_amount.assert_called_once_with({
        "Сумма операции": 100,
        "Валюта операции": "USD"
    })
