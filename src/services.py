import json

from src.utils import filter_by_date, filter_by_state


def get_cashback_categories(operations_list: list[dict]) -> list[str]:
    """
    Функция - вспомогательная для get_profitable_cashback_categories, получает список транзакций
    Возвращает список всех категорий кэшбэка, которые есть во входном списке
    """
    cashback_categories = list(set(transaction.get("Категория") for transaction in operations_list))
    cashback_categories.sort()

    return cashback_categories





def get_profitable_cashback_categories(year: int, month: int, operations_list: list[dict]):
    """
    Сервис «Выгодные категории повышенного кешбэка» позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кешбэка.
    Функция сервиса принимает год, месяц для расчета и транзакции в формате списка словарей.
    Возвращает JSON-ответ с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года.
    Формат выходных данных:
    {
        "Категория 1": 1000,
        "Категория 2": 2000,
        "Категория 3": 500
    }
    """
    dict_to_json = dict()
    start_date_operations = f"01.{month}.{year} 00:00:00"
    end_date_operations = f"31.{month}.{year} 23:59:59"

    # отфильтровываем операции с нужными датами
    operations = filter_by_date(operations_list, start_date_operations, end_date_operations)

    # отфильтровываем только операции со статусом ОК
    operations = filter_by_state(operations)

    cashback_categories = get_cashback_categories(operations)

    pass

if __name__ == '__main__':
    print()
