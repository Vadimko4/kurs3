import pytest
from unittest.mock import patch

from src.views import get_cards_information, get_top_five_transactions


def test_get_cards_information(test_rub_operation_list):
    #  для теста используем только рублёвые транзакции
    assert get_cards_information(test_rub_operation_list) == [
        {
            'last_digits': '4556',
            'total_spent': 14750.0,
            'cashback': 99.0
        },
        {
            'last_digits': '7197',
            'total_spent': -283.0,
            'cashback': 0
        }
    ]


def test_get_top_five_transactions(test_rub_operation_list):

    assert (get_top_five_transactions(test_rub_operation_list) ==
            [
                {
                    'date': '22.07.2021',
                    'amount': -96099.94,
                    'category': 'Переводы',
                    'description': 'Перевод Кредитная карта. ТП 10.2 RUR'
                },
                {
                    'date': '22.07.2021',
                    'amount': -90000.0,
                    'category': 'Переводы',
                    'description': 'Перевод с карты'
                },
                {
                    'date': '22.07.2021',
                    'amount': -90000.0,
                    'category': 'Переводы',
                    'description': 'Перевод с карты'
                },
                {
                    'date': '26.07.2021',
                    'amount': -250.0,
                    'category': 'Связь',
                    'description': 'МТС'
                },
                {
                    'date': '23.07.2021',
                    'amount': -200.0,
                    'category': 'Фастфуд',
                    'description': 'Pyshechnaya Pyshlandiya'
                }
            ])
