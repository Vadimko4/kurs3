from unittest.mock import patch

import pytest

from src.external_api import get_rub_transaction_amount


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
