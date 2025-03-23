import pandas as pd

from utils import (PATH_TO_OPERATIONS_XLSX_FILE, get_operations_from_xlsx, filter_by_state, filter_by_date,
                   filter_by_card, get_card_total_rub_spent, get_card_cashback_rub,
                   PATH_TO_USER_SETTINGS_JSON_FILE, get_currency_list_from_json, get_stock_list_from_json)
from external_api import get_rub_transaction_amount, get_currency_too_rub_rate


def get_cards_information(operations_list: list[dict]) -> list[dict]:
    """
    Принимает список словарей с данными о банковских операциях;
    возвращает список словарей, содержащих сводную информацию по картам, которые фигурируют
    во входном списке операций: последние 4 цифры номера карты, общая сумма расходов,
    сумма кешбэка
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


def get_stock_prices(date: str) -> list[dict]:
    pass


if __name__ == '__main__':
    request_date = input("Введите интересующую Вас дату: ")
    start_date_operation = f"01{request_date[2:]} 00:00:00"
    end_date_operation = f"{request_date} 23:59:59"
    operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)

    # отфильтровываем только операции со статусом ОК
    operations = filter_by_state(operations)

    # отфильтровываем операции с нужными датами
    operations = filter_by_date(operations, start_date_operation, end_date_operation)

    print(get_cards_information(operations))
    print(get_top_five_transactions(operations))

    # получаем список валют пользователя
    currencies = get_currency_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
    print(get_currency_rates(currencies))

    # получаем список акций пользователя
    stocks = get_stock_list_from_json(PATH_TO_USER_SETTINGS_JSON_FILE)
