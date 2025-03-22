import pandas as pd

from utils import (PATH_TO_OPERATIONS_XLSX_FILE, get_operations_from_xlsx, filter_by_state, filter_by_date,
                   filter_by_card, get_card_total_rub_spent, get_card_cashback_rub)


def get_cards_information(operations_list: list[dict], start_date: str, end_date) -> list[dict]:
    """
    Принимает список словарей с данными о банковских операциях, и целевую дату - с начала месяца по которую
    нужно сформировать отчёт;
    возвращает список словарей, содержащих сводную информацию по картам, которые фигурируют
    во входном списке операций: последние 4 цифры номера карты, общая сумма расходов,
    кешбэк (1 рубль на каждые 100 рублей)
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
    pass


def get_currency_rates(date: str) -> list[dict]:
    pass


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
    print(get_cards_information(operations, start_date_operation, end_date_operation))
