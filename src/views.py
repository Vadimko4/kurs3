import pandas as pd
from utils import filter_by_state, PATH_TO_OPERATIONS_XLSX_FILE, get_operations_from_xlsx


def get_cards_information(operations_list: list[dict]) -> list[dict]:
    """
    Принимает список словарей с данными о банковских операциях,
    возвращает список словарей, содержащих сводную информацию по картам, которые фигурируют
    во входном списке операций: последние 4 цифры номера карты, общая сумма расходов,
    кешбэк (1 рубль на каждые 100 рублей)
    """
    # отфильтровываем только операции со статусом ОК
    operations_list = filter_by_state(operations_list)

    # получаем номера карт, убиваем nan
    cards_list = list(set(i.get("Номер карты") for i in operations_list if pd.notna(i.get("Номер карты"))))

    return cards_list


if __name__ == '__main__':
    operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)
    print(get_cards_information(operations))
