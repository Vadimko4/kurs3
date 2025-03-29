import pandas as pd
import datetime

from src.views import get_views_json
from src.services import get_profitable_cashback_categories
from src.utils import (get_greeting, get_operations_from_xlsx, PATH_TO_OPERATIONS_XLSX_FILE,
                       filter_by_state, filter_by_date)
from src.reports import spending_by_category


def foolproof_user_date_input() -> str:
    """
    Функция опрашивает пользователя с клавиатуры и возвращает целевую дату для анализа банковских транзакций
    в виде: dd.mm.yyyy
    """
    while True:
        user_answer = input('\nПользователь: ')
        dd = user_answer[:2]
        mm = user_answer[3:5]
        yyyy = user_answer[-4:]
        if (len(user_answer) != 10 or any(not i.isdigit() for i in (dd, mm, yyyy)) or int(dd) not in range(32)
                or int(mm) not in range(1, 13) or user_answer.count('.') != 2):
            print("\nПрограмма: Неверный ввод, должна быть строка вида dd.mm.yyyy \nПопробуйте ещё раз")
        else:
            break
    return user_answer


def foolproof_user_cashback_date_input() -> str:
    """
    Функция опрашивает пользователя с клавиатуры и возвращает год и месяц для анализа банковских транзакций
    на предмет наиболее выгодного кэшбэка - в виде: yyyy.mm
    """
    while True:
        user_answer = input('\nПользователь: ')
        yyyy = user_answer[:4]
        mm = user_answer[-2:]
        if (len(user_answer) != 7 or any(not i.isdigit() for i in (mm, yyyy))
                or int(mm) not in range(1, 13) or user_answer.count('.') != 1):
            print("\nПрограмма: Неверный ввод, должна быть строка вида yyyy.mm \nПопробуйте ещё раз")
        else:
            break
    return user_answer


if __name__ == '__main__':
    # print(f"Программа: {get_greeting()}")
    # print("\nВведите интересующую Вас дату (строка вида dd.mm.yyyy)")
    # req_date_str = foolproof_user_date_input()
    # req_date_str += " 23:59:59"
    # req_date = datetime.datetime.strptime(req_date_str, "%d.%m.%Y %H:%M:%S")
    #
    # print('\nПрограмма: Идёт формирование ответа на ваш запрос...')
    # # формируем json ответ
    # json_views_answer = get_views_json(req_date)
    # print(json_views_answer)

    print("\nПрограмма: перейдём к другим услугам.")
    print("Давайте посмотрим, какие категории для вас наиболее выгодны в плане повышенного кэшбэка.")
    print("Введите год и месяц для анализа (строка вида yyyy.mm)")
    req_date_str = foolproof_user_cashback_date_input()
    print('\nПрограмма: Идёт формирование ответа на ваш запрос...')
    ops_list = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)

    yyyy = int(req_date_str[:4])
    mm = int(req_date_str[-2:])
    json_services_answer = get_profitable_cashback_categories(yyyy, mm, ops_list)
    print(json_services_answer)

    print("\nПрограмма: Бог троицу любит)")
    print("Давайте посмотрим, сколько денег вы потратили по какой-нибудь конкретной категории за три месяца.")

    print("\nЕсли хотите посмотреть статистику за последние три месяца от сегодняшней даты, то просто нажмите <ENTER>")
    print("или введите что угодно, если хотите ввести конкретную дату - наберите слово <дата>")
    user_answ = input("\nПользователь: ").lower()

    req_date = None
    if user_answ == 'дата':
        print("\nВведите интересующую Вас дату (строка вида dd.mm.yyyy)")
        req_date = foolproof_user_date_input()

    print("\nПрограмма: Какая категория расходов вас интересует?")
    ctg = input("\nПользователь: ").title()

    print('\nПрограмма: Идёт формирование ответа на ваш запрос...')
    # transactions_dataframe = pd.read_excel(PATH_TO_OPERATIONS_XLSX_FILE)
    transactions_dataframe = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    json_reports_answer = spending_by_category(transactions_dataframe, ctg, req_date)
    print('\nПрограмма: Отчёт успешно сформирован и записан в xslsx файл в папку reports')
    print('Всего доброго!')
