import pytest

from src.views import get_cards_information


def test_get_cards_information(test_operation_list):
    #  для теста оставляем только рублёвые транзакции
    test_list = test_operation_list[:5:2]
    test_list.extend(test_operation_list[5:8:2])
    test_list.extend(test_operation_list[8:14])
    assert get_cards_information(test_list) == [
        {
            'last_digits': '7197',
            'total_spent': -283.0,
            'cashback': 0
        },
        {
            'last_digits': '4556',
            'total_spent': 14750.0,
            'cashback': 99.0}
    ]
