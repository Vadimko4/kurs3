import os

import pandas as pd
import numpy as np
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


def get_date_obj_from_str_date(str_date: str) -> datetime:
    """
    переводит строковое отображение даты вида '26.07.2021 20:35:57' 
    в объект библиотеки datetime
    """
    if len(str_date) == 10:  # дата вида 26.07.2021 - временнАя часть отсутствует
        str_date = f"{str_date} 00:00:00"

    year = int(str_date.split()[0].split('.')[2])
    month = int(str_date.split()[0].split('.')[1])
    day = int(str_date.split()[0].split('.')[0])
    hour = int(str_date.split()[1].split(':')[0])
    minute = int(str_date.split()[1].split(':')[1])
    second = int(str_date.split()[1].split(':')[2])
    result_date = datetime.datetime(year, month, day, hour, minute, second)
    return result_date
    
    
def filter_by_date(operations_list: list[dict], start_date_str: str, end_date_str: str) -> list[dict]:
    """
    фильтрует список операций по дате: от start_data включительно, до end_data включительно
    """
    # убираем транзакции, в которых нет ключа "Дата операции"
    operations_list = [i for i in operations_list if not i.get('Дата операции') is None]

    start_data = get_date_obj_from_str_date(start_date_str)
    end_data = get_date_obj_from_str_date(end_date_str)

    result_list = []
    for operation in operations_list:
        str_date = operation.get('Дата операции')
        operation_date = get_date_obj_from_str_date(str_date)
        if start_data <= operation_date <= end_data:
            result_list.append(operation)

    return result_list


def filter_by_card(operations_list: list[dict], card_number: str) -> list[dict]:
    """
    фильтрует список операций по номеру карты
    """
    # убираем транзакции, в которых нет ключа "Номер карты"
    operations_list = [i for i in operations_list if not i.get('Номер карты') is None]

    operations_list = [i for i in operations_list if i.get('Номер карты') == card_number]
    return operations_list


def get_card_total_rub_spent(operations_list: list[dict]) -> float:
    """
    Из списка операций возращает суммарные траты в рублях по всем картам, которые представлены в списке
    """
    total_spent_sum = sum(get_rub_transaction_amount(i) for i in operations_list)

    return total_spent_sum


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
    operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    # operations = filter_by_state(operations, 'FAILED')
    print(get_card_cashback_rub(operations[874: 894]))  # [874: 894], кэшбэк есть с 831
