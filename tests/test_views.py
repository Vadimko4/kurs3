import pandas as pd

from src.views import get_cards_information, get_top_five_transactions


def test_get_cards_information(test_rub_operation_list):
    #  для теста используем только рублёвые транзакции
    assert get_cards_information(pd.DataFrame(test_rub_operation_list)) == [
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

    assert (get_top_five_transactions(pd.DataFrame(test_rub_operation_list)) ==
            [
                {
                    'date': '22.07.2021 23:56:18', 'amount': -96099.94, 'category': 'Переводы',
                    'description': 'Перевод Кредитная карта. ТП 10.2 RUR'
                },
                {
                    'date': '22.07.2021 23:54:43', 'amount': -90000.0, 'category': 'Переводы',
                    'description': 'Перевод с карты'
                },
                {
                    'date': '22.07.2021 23:53:25', 'amount': -90000.0, 'category': 'Переводы',
                    'description': 'Перевод с карты'
                },
                {
                    'date': '26.07.2021 20:35:57', 'amount': -250.0, 'category': 'Связь', 'description': 'МТС'
                },
                {
                    'date': '23.07.2021 16:01:01', 'amount': -200.0, 'category': 'Фастфуд',
                    'description': 'Pyshechnaya Pyshlandiya'
                },
                {
                    'date': '25.07.2021 20:55:58', 'amount': -43.0, 'category': 'Транспорт',
                    'description': 'Северо-Западная пригородная пассажирская компания'
                }
            ])
