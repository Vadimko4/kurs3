import pandas as pd
import numpy as np
import json

from src.utils import (filter_by_card, get_card_total_rub_spent, get_card_cashback_rub, get_greeting,
                       PATH_TO_USER_SETTINGS_JSON_FILE, get_currency_list_from_json, get_stock_list_from_json)
from src.external_api import get_rub_transaction_amount, get_currency_too_rub_rate, get_stock_rub_price


def get_cards_information(operations_list: list[dict]) -> list[dict]:
    """
    Принимает список словарей с данными о банковских операциях;
    возвращает список словарей, содержащих сводную информацию по картам, которые фигурируют
    во входном списке операций: последние 4 цифры номера карты, общая сумма расходов,
    сумма кешбэка
    Функция считает по всем транзакциям, не обращает внимание на статус и дату операции
    Предполагается, что по статусу и дате операции были отфильтрованы ранее
    """
    # получаем номера карт, убиваем nan
    card_numbers_list = list(set(i.get("Номер карты") for i in operations_list if pd.notna(i.get("Номер карты"))))

    # Формируем общую информацию по всем картам
    cards_information_list = []
    for card_number in card_numbers_list:
        card_information_dict = dict()
        one_card_operations_list = filter_by_card(operations_list, card_number)

        card_information_dict["last_digits"] = card_number[1:]
        card_information_dict["total_spent"] = get_card_total_rub_spent(one_card_operations_list)
        card_information_dict["cashback"] = get_card_cashback_rub(one_card_operations_list)

        cards_information_list.append(card_information_dict)
    return cards_information_list


def get_top_five_transactions(operations_list: list[dict]) -> list[dict]:
    """
    Принимает список словарей с данными о банковских операциях;
    возвращает список словарей, содержащих сводную информацию по топ-5 самых больших расходов
    за указанный период в виде:
    "date": "20.12.2021",
    "amount": 829.00,
    "category": "Супермаркеты",
    "description": "Лента"
    """
    #  Сортируем транзакции по возрастанию "Сумма операции" в рублёвом эквиваленте
    sorted_operations_list = sorted(operations_list, key=lambda x: get_rub_transaction_amount(x))

    top_five_list = []
    for i in range(5):
        top_op_dict = dict()
        top_op_dict["date"] = sorted_operations_list[i].get('Дата операции')[:10]
        top_op_dict["amount"] = get_rub_transaction_amount(sorted_operations_list[i])
        top_op_dict["category"] = sorted_operations_list[i].get('Категория')
        top_op_dict["description"] = sorted_operations_list[i].get('Описание')
        top_five_list.append(top_op_dict)

    return top_five_list


def get_currency_rates(currency_list: list[str]) -> list[dict]:
    """
    Принимает список валют;
    возвращает список словарей, курсы валют к рублю в виде:
    "currency": "USD",
    "rate": 73.21
    """
    currency_rates = [{"currency": currency, "rate": get_currency_too_rub_rate(currency)} for currency in currency_list]
    return currency_rates


def get_stock_prices(stock_list) -> list[dict]:
    """
    Принимает список акций;
    возвращает список словарей, стоимость акции в рублях в виде:
    "stock": "AAPL",
    "price": 150.12
    """
    stock_prices = [{"stock": stock, "price": get_stock_rub_price(stock)} for stock in stock_list]
    return stock_prices


def get_views_json(transactions: list[dict]):
    """
    Основная функция модуля. Анализирует список транзакций.
    По результатам анализа возвращает json в который запакован словарь.
    В словаре следующие ключи:

    "greeting" - приветствие, адекватно времени обращения к функции

    "cards" - информация по картам, список словарей вида:
    "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62

    "top_transactions" - 5 самых больших расходов за период в виде:
    "date": "20.12.2021",
    "amount": 829.00,
    "category": "Супермаркеты",
    "description": "Лента"

    "currency_rates" - курсы валют (берутся из user_settings.json файла) к рублю список словарей вида:
    "currency": "USD",
    "rate": 73.21

    "stock_prices" - стоимость акций (берутся из user_settings.json файла) в рублях в виде:
    "stock": "AAPL",
    "price": 150.12
    """
    dict_to_json = dict()

    dict_to_json["greeting"] = get_greeting()
    dict_to_json["cards"] = get_cards_information(transactions)
    dict_to_json["top_transactions"] = get_top_five_transactions(transactions)

    # получаем список валют пользователя
    currencies = get_currency_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    dict_to_json["currency_rates"] = get_currency_rates(currencies)

    # получаем список акций пользователя
    stocks = get_stock_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    dict_to_json["stock_prices"] = get_stock_prices(stocks)

    json_data = json.dumps(dict_to_json, ensure_ascii=False, indent=4)
    return json_data


if __name__ == '__main__':
    ops = [
        {
            'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
            'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -250.0,
            'Валюта операции': 'RUB', 'Сумма платежа': -250.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': 99.0, 'Категория': 'Связь',
            'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
        },
        {
            'Дата операции': '25.07.2021 20:55:58', 'Дата платежа': '26.07.2021',
            'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -43.0,
            'Валюта операции': 'RUB', 'Сумма платежа': -43.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Транспорт',
            'MCC': 4111.0,  'Описание': 'Северо-Западная пригородная пассажирская компания',
            'Бонусы (включая кэшбэк)': 0,  'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 43.0
        },
        {
            'Дата операции': '23.07.2021 19:05:27',
            'Дата платежа': '23.07.2021', 'Номер карты': np.nan,
            'Статус': 'OK', 'Сумма операции': 5300.0, 'Валюта операции': 'RUB',
            'Сумма платежа': 5300.0, 'Валюта платежа': 'RUB', 'Кэшбэк': np.nan,
            'Категория': 'Пополнения', 'MCC': 6012.0, 'Описание': 'Перевод с карты',
            'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 5300.0
        },
        {
            'Дата операции': '23.07.2021 19:00:53', 'Дата платежа': '23.07.2021',
            'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': 15000.0,
            'Валюта операции': 'RUB', 'Сумма платежа': 15000.0, 'Валюта платежа': 'RUB',
            'Кэшбэк': np.nan, 'Категория': 'Пополнения', 'MCC': np.nan,
            'Описание': 'Внесение наличных через банкомат Тинькофф',
            'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 15000.0
        },
        {
            'Дата операции': '23.07.2021 16:05:51', 'Дата платежа': '23.07.2021',
            'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -40.0, 'Валюта операции': 'RUB',
            'Сумма платежа': -40.0, 'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Фастфуд',
            'MCC': 5814.0, 'Описание': 'Pyshechnaya Pyshlandiya', 'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 40.0
        },
        {
            'Дата операции': '23.07.2021 16:01:01', 'Дата платежа': '23.07.2021',
            'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -200.0, 'Валюта операции': 'RUB',
            'Сумма платежа': -200.0, 'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Фастфуд',
            'MCC': 5814.0, 'Описание': 'Pyshechnaya Pyshlandiya', 'Бонусы (включая кэшбэк)': 4,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 200.0
        },
        {
            'Дата операции': '22.07.2021 23:56:19', 'Дата платежа': '23.07.2021', 'Номер карты': np.nan,
            'Статус': 'OK', 'Сумма операции': 96099.94, 'Валюта операции': 'RUB', 'Сумма платежа': 96099.94,
            'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Переводы', 'MCC': np.nan,
            'Описание': 'Перевод Кредитная карта. ТП 10.2 RUR', 'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 96099.94
        },
        {
            'Дата операции': '22.07.2021 23:56:18', 'Дата платежа': '23.07.2021', 'Номер карты': np.nan,
            'Статус': 'OK', 'Сумма операции': -96099.94, 'Валюта операции': 'RUB', 'Сумма платежа': -96099.94,
            'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Переводы', 'MCC': np.nan,
            'Описание': 'Перевод Кредитная карта. ТП 10.2 RUR', 'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 96099.94
        },
        {
            'Дата операции': '22.07.2021 23:55:04', 'Дата платежа': '23.07.2021', 'Номер карты': np.nan,
            'Статус': 'OK', 'Сумма операции': 90000.0, 'Валюта операции': 'RUB', 'Сумма платежа': 90000.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Пополнения', 'MCC': 6012.0,
            'Описание': 'Перевод с карты', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 90000.0
        },
        {
            'Дата операции': '22.07.2021 23:54:43', 'Дата платежа': np.nan, 'Номер карты': np.nan,
            'Статус': 'OK', 'Сумма операции': -90000.0, 'Валюта операции': 'RUB', 'Сумма платежа': -90000.0,
            'Валюта платежа': 'RUB', 'Кэшбэк': np.nan, 'Категория': 'Переводы', 'MCC': np.nan,
            'Описание': 'Перевод с карты', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 90000.0
        },
        {
            'Дата операции': '22.07.2021 23:53:25', 'Дата платежа': np.nan, 'Номер карты': np.nan, 'Статус': 'FAILED',
            'Сумма операции': -90000.0, 'Валюта операции': 'RUB', 'Сумма платежа': -90000.0, 'Валюта платежа': 'RUB',
            'Кэшбэк': np.nan, 'Категория': 'Переводы', 'MCC': np.nan, 'Описание': 'Перевод с карты',
            'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 90000.0
        }
        ]
    print(get_top_five_transactions(ops))
    # print(get_views_json())

    # req_date = input("Введите интересующую Вас дату: ")
    # start_date = f"01{req_date[2:]} 00:00:00"
    # end_date = f"{req_date} 23:59:59"
    # transactions = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    #
    # # отфильтровываем только операции со статусом ОК
    # transactions = filter_by_state(transactions)
    #
    # # отфильтровываем операции с нужными датами
    # transactions = filter_by_date(transactions, start_date, end_date)
    #
    # print(get_cards_information(transactions))
    # print(get_top_five_transactions(transactions))
    #
    # # получаем список валют пользователя
    # currs = get_currency_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    # print(get_currency_rates(currs))
    #
    # # получаем список акций пользователя
    # st = get_stock_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    # print(get_stock_prices(st))
