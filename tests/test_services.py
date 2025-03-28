import json

from src.services import get_categories, get_profitable_cashback_categories


def test_get_categories(test_rub_operation_list):
    assert (get_categories(test_rub_operation_list) ==
            ['Связь', 'Транспорт', 'Фастфуд'])
    assert get_categories(test_rub_operation_list[2:4]) == []
    assert get_categories([]) == []


def test_get_profitable_cashback_categories(test_rub_operation_list):
    assert (json.loads(get_profitable_cashback_categories(2021, 7, test_rub_operation_list)) ==
            {"Связь": 3.0, "Фастфуд": 3.0, "Транспорт": 1.0})
