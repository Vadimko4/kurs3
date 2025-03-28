import datetime
import json
import os

import numpy as np
import pandas as pd

from src.external_api import get_rub_transaction_amount
from src.logger import utils_logger

PATH_TO_OPERATIONS_XLSX_FILE = os.path.join(os.path.dirname(__file__)[:-4], "data", "operations.xlsx")
PATH_TO_USER_SETTINGS_JSON_FILE = os.path.join(os.path.dirname(__file__)[:-4], "data", "user_settings.json")


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
        utils_logger.info('Успешное чтение списка операций из xlsx файла')

    except Exception as e:
        transactions_list = []
        utils_logger.error(f'При чтении списка операций из xlsx файла произошла ошибка: {e}', exc_info=True)

    if not transactions_list:
        utils_logger.warning('Из xlsx файла считан пустой список')
    return transactions_list


def get_currency_list_from_json(file_name: str = '') -> list[str]:
    """
    Функция принимает на вход путь до JSON-файла,
    считывает из него и возвращает список валют пользователя
    """
    try:
        with open(file_name, encoding='utf-8') as f:
            list_of_currency = json.load(f).get("user_currencies")
        utils_logger.info('Успешное чтение списка валют из json файла')

    except Exception as e:
        list_of_currency = []
        utils_logger.error(f'При чтении списка валют из json файла произошла ошибка: {e}', exc_info=True)

    if not list_of_currency:
        utils_logger.warning('Список валют пользователя пуст')
    return list_of_currency


def get_stock_list_from_json(file_name: str = '') -> list[str]:
    """
    Функция принимает на вход путь до JSON-файла,
    считывает из него и возвращает список валют пользователя
    """
    try:
        with open(file_name, encoding='utf-8') as f:
            list_of_stocks = json.load(f).get("user_stocks")
        utils_logger.info('Успешное чтение списка акций из json файла')

    except Exception as e:
        list_of_stocks = []
        utils_logger.error(f'При чтении списка акций из json файла произошла ошибка: {e}', exc_info=True)

    if not list_of_stocks:
        utils_logger.warning('Список акций пользователя пуст')
    return list_of_stocks


def filter_by_state(operations_list: list[dict], state: str = 'OK') -> list[dict]:
    """
    Принимает список всех операций - возвращает только те, у которых статус = state
    По умолчанию статус равен ОК
    """
    # убираем транзакции, в которых нет ключа "state"
    operations_list = [i for i in operations_list if not i.get('Статус') is None]

    if state not in ['OK', 'FAILED']:
        utils_logger.error('При сортировке транзакций по статусу произошла ошибка: Ошибочный статус операции!')
        raise ValueError('Ошибочный статус операции!')

    operations_list = [operation for operation in operations_list if operation.get('Статус') == state]
    utils_logger.info(f"Транзакции отсортированы по статусу {state}")

    if not operations_list:
        utils_logger.warning("Список транзакций пуст")

    return operations_list


# def get_date_obj_from_str_date(str_date: str) -> datetime:
#     """
#     переводит строковое отображение даты вида '26.07.2021 20:35:57'
#     в объект библиотеки datetime
#     """
#     if len(str_date) == 10:  # дата вида 26.07.2021 - временнАя часть отсутствует
#         str_date = f"{str_date} 00:00:00"
#
#     year = int(str_date.split()[0].split('.')[2])
#     month = int(str_date.split()[0].split('.')[1])
#     day = int(str_date.split()[0].split('.')[0])
#     hour = int(str_date.split()[1].split(':')[0])
#     minute = int(str_date.split()[1].split(':')[1])
#     second = int(str_date.split()[1].split(':')[2])
#     result_date = datetime.datetime(year, month, day, hour, minute, second)
#     return result_date


def filter_by_date(operations_list: list[dict], start_date: datetime, end_date: datetime) -> list[dict]:
    """
    фильтрует список операций по дате: от start_data включительно, до end_data включительно
    """
    # убираем транзакции, в которых нет ключа "Дата операции"
    operations_list = [i for i in operations_list if not i.get('Дата операции') is None]

    # start_data = get_date_obj_from_str_date(start_date_str)
    # end_data = get_date_obj_from_str_date(end_date_str)

    result_list = []
    for operation in operations_list:
        str_date = operation.get('Дата операции')
        # operation_date = get_date_obj_from_str_date(str_date)
        operation_date = datetime.datetime.strptime(str_date, "%d.%m.%Y %H:%M:%S")
        if start_date <= operation_date <= end_date:
            result_list.append(operation)

    utils_logger.info('Транзакции отсортированы по дате')

    if not result_list:
        utils_logger.warning("Список транзакций пуст")

    return result_list


def filter_by_card(operations_list: list[dict], card_number: str) -> list[dict]:
    """
    фильтрует список операций по номеру карты
    """
    # убираем транзакции, в которых нет ключа "Номер карты"
    operations_list = [i for i in operations_list if not i.get('Номер карты') is None]

    operations_list = [i for i in operations_list if i.get('Номер карты') == card_number]
    return operations_list


def filter_by_category(operations_list: list[dict], category: str) -> list[dict]:
    """
    фильтрует список операций по указанной в параметре category категории
    """
    # убираем транзакции, в которых нет ключа "Категория"
    operations_list = [i for i in operations_list if not i.get('Категория') is None]

    operations_list = [i for i in operations_list if i.get('Категория') == category]
    return operations_list


def get_total_rub_spent(operations_list: list[dict]) -> float:
    """
    Из списка операций возращает суммарные траты в рублях по всем операциям, которые представлены в списке
    """
    total_spent_sum = sum(get_rub_transaction_amount(i) for i in operations_list)

    return round(total_spent_sum, 2)


def get_card_cashback_rub(operations_list: list[dict]) -> float:
    """
    Из списка операций возращает суммарный кешбэк в рублях.
    Так как он представлен только в рублях - перевод из иностранной валюты не производится
    """
    # убираем транзакции, в которых нет ключа "Кэшбэк" или он есть, но пустой (nan)
    operations_list = [i for i in operations_list if (not i.get('Кэшбэк') is None) and
                       (not np.isnan(i.get('Кэшбэк', np.nan)))]  # как обрабатывать nan

    cashback_sum = sum(i.get('Кэшбэк') for i in operations_list)

    return round(cashback_sum, 2)


if __name__ == '__main__':
    # print(get_greeting())
    # curr_list = get_currency_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    # st_list = get_stock_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    # print(curr_list)
    # print(st_list)

    # operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    # operations = filter_by_state(operations, 'FAILED')
    # print(get_card_cashback_rub(operations[874: 894]))  # [874: 894], кэшбэк есть с 831
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
    date1 = datetime.datetime(2022, 7, 26, 0, 0,  0 )
    date2 = datetime.datetime(2022, 7, 27, 0, 0,  0 )
    print(filter_by_date(ops, date1, date2))
    # cats = filter_by_category(ops, 'Транспорт')
    # print(len(cats), '\n', cats)
    #
    # excel_data = pd.read_excel(PATH_TO_OPERATIONS_XLSX_FILE)
    # print(type(excel_data))
