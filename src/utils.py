import os

import pandas as pd
import datetime

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
    #hh = 10

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


def filter_by_state(operations: list[dict], state: str = 'OK') -> list[dict]:
    """
    Принимает список всех операций - возвращает только те, у которых статус = state
    По умолчанию статус равен ОК
    """
    # убираем транзакции, в которых нет ключа "state"
    operations = [i for i in operations if not i.get('Статус') is None]

    if state not in ['OK', 'FAILED']:
        raise ValueError('Ошибочный статус операции!')

    return [operation for operation in operations if operation.get('Статус') == state]


if __name__ == '__main__':
    print(get_greeting())
    operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    #operations = filter_by_state(operations, 'FAILED')
    print(operations[874: 894])
