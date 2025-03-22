import os

import pandas as pd
# from collections import Counter
import datetime
from src.external_api import get_rub_transaction_amount

PATH_TO_OPERATIONS_XLSX_FILE = os.path.join(os.path.dirname(__file__)[:-4], "data", "operations.xlsx")


def get_greeting() -> str:
    """
    Возвращает адекватное приветствие, в зависимости от времени вызова:
    (4:01 - 11:00) Доброе утро!/(11:01 - 17:00) Добрый день!/
    (17:01 - 23:00) Добрый вечер!/(23:01 - 5:00) Доброй ночи!
    """
    current_date_time = datetime.datetime.now()
    hh = current_date_time.hour
    mm = current_date_time.minute
    ss = current_date_time.second

    if hh in range(5, 11) or (hh == 4 and (mm > 0 or ss > 0)) or (hh == 11 and (mm == 0 or ss == 0)):
        greeting = 'Доброе утро!'
    elif hh in range(12, 17) or (hh == 11 and (mm > 0 or ss > 0)) or (hh == 17 and (mm == 0 or ss == 0)):
        greeting = 'Добрый день!'
    elif hh in range(18, 23) or (hh == 17 and (mm > 0 or ss > 0)) or (hh == 23 and (mm == 0 or ss == 0)):
        greeting = 'Добрый вечер!'
    else:
        greeting = 'Доброй ночи!'
    return greeting


def get_operations_from_xlsx(xlsx_file_name: str) -> list[dict]:
    """
    считывает список транзакций-операций (словари) из xlsx файла
    """
    try:
        excel_data = pd.read_excel(xlsx_file_name)
        transactions_list = excel_data.to_dict(orient='records')

    except Exception:
        transactions_list = []

    return transactions_list


def filter_by_state(operations_list: list[dict], state: str = 'OK') -> list[dict]:
    """
    Принимает список всех операций - возвращает только те, у которых статус = state
    По умолчанию статус равен ОК
    """
    # убираем транзакции, в которых нет ключа "state"
    operations_list = [i for i in operations_list if not i.get('Статус') is None]

    if state not in ['OK', 'FAILED']:
        raise ValueError('Ошибочный статус операции!')

    return [operation for operation in operations_list if operation.get('Статус') == state]


def filter_by_date(operations_list: list[dict], start_data: datetime, end_data: datetime) -> list[dict]:
    """
    фильтрует список операций по дате: от start_data включительно, до end_data включительно
    """
    # убираем транзакции, в которых нет ключа "Дата платежа"
    operations_list = [i for i in operations_list if not i.get('Дата операции') is None]

    result_list = []
    for operation in operations_list:
        str_operation_date = operation.get('Дата операции')
        year = int(str_operation_date.split()[0].split('.')[2])
        month = int(str_operation_date.split()[0].split('.')[1])
        day = int(str_operation_date.split()[0].split('.')[0])
        hour = int(str_operation_date.split()[1].split(':')[0])
        minute = int(str_operation_date.split()[1].split(':')[1])
        second = int(str_operation_date.split()[1].split(':')[2])
        operation_date = datetime.datetime(year, month, day, hour, minute, second)
        if start_data <= operation_date <= end_data:
            result_list.append(operation)

    return result_list


def filter_by_card(operations_list: list[dict], card_number: str) -> list[dict]:
    """
    фильтрует список операций по номеру карты
    """
    pass


def get_card_total_rub_spent(operations_list: list[dict]) -> float:
    """
    Из списка операций возращает суммарные траты в рублях по указанной карте
    """
    total_spent_sum = sum(get_rub_transaction_amount(i) for i in operations_list)

    return total_spent_sum


# def get_categories_count(operations_list: list[dict], categories_list: list[str]) -> dict:
#     """
#     Принимает список словарей с данными о банковских операциях и список интересующих нас ключей операций,
#     dозвращает словарь, в котором ключи — названия интересующих нас ключей, значения — количество операций
#     в каждой категории
#     """
#     # оставляем только те операции, у которых описание в "description" содержится в categories_list
#     operations_list = [i.get("description") for i in operations_list if i.get("description") in categories_list]
#
#     return Counter(operations_list)


if __name__ == '__main__':
    print(get_greeting())
    # operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    # operations = filter_by_state(operations, 'FAILED')
    # print(operations[874: 894])
    print(get_card_total_rub_spent(
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
                'Валюта операции': 'TRY', 'Сумма платежа': -135.0, 'Валюта платежа': 'TRY',
                'Кэшбэк': None, 'Категория': 'Фастфуд', 'MCC': 5814.0, 'Описание': 'Pingvin Kofe I Chaj',
                'Бонусы (включая кэшбэк)': 2, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 135.0
            },
            {
                'Дата операции': '25.07.2021 20:55:58', 'Дата платежа': '26.07.2021',
                'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -43.0,
                'Валюта операции': 'RUB', 'Сумма платежа': -43.0,
                'Валюта платежа': 'RUB', 'Кэшбэк': None, 'Категория': 'Транспорт',
                'MCC': 4111.0, 'Описание': 'Северо-Западная пригородная пассажирская компания',
                'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 43.0
            },
            {
                'Дата операции': '23.07.2021 19:16:13', 'Дата платежа': '23.07.2021',
                'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -541.5,
                'Валюта операции': 'EUR', 'Сумма платежа': -541.5,
                'Валюта платежа': 'EUR', 'Кэшбэк': None, 'Категория': 'Супермаркеты',
                'MCC': 5411.0, 'Описание': 'Prisma', 'Бонусы (включая кэшбэк)': 10,
                'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 541.5
            },
            {
                'Дата операции': '23.07.2021 19:05:27',
                'Дата платежа': '23.07.2021', 'Номер карты': None,
                'Статус': 'OK', 'Сумма операции': 5300.0, 'Валюта операции': 'RUB',
                'Сумма платежа': 5300.0, 'Валюта платежа': 'RUB', 'Кэшбэк': None,
                'Категория': 'Пополнения', 'MCC': 6012.0, 'Описание': 'Перевод с карты',
                'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 5300.0
            },
            {
                'Дата операции': '23.07.2021 19:00:53', 'Дата платежа': '23.07.2021',
                'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': 15000.0,
                'Валюта операции': 'RUB', 'Сумма платежа': 15000.0, 'Валюта платежа': 'RUB',
                'Кэшбэк': None, 'Категория': 'Пополнения', 'MCC': None,
                'Описание': 'Внесение наличных через банкомат Тинькофф',
                'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 15000.0
            },
            {
                'Дата операции': '23.07.2021 18:51:35', 'Дата платежа': '23.07.2021',
                'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -82.0,
                'Валюта операции': 'USD', 'Сумма платежа': -82.0, 'Валюта платежа': 'USD',
                'Кэшбэк': None, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Колхоз',
                'Бонусы (включая кэшбэк)': 1, 'Округление на инвесткопилку': 0,
                'Сумма операции с округлением': 82.0
            }]
    ))
