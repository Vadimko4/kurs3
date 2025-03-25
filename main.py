from src.views import get_views_json
from src.utils import (get_greeting, get_operations_from_xlsx, PATH_TO_OPERATIONS_XLSX_FILE,
                       filter_by_state, filter_by_date)


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


if __name__ == '__main__':
    print(f"Программа: {get_greeting()}")
    print("\nВведите интересующую Вас дату (строка вида dd.mm.yyyy)")
    request_date = foolproof_user_date_input()

    print('\nПрограмма: Идёт формирование ответа на ваш запрос...')
    start_date_operation = f"01{request_date[2:]} 00:00:00"
    end_date_operation = f"{request_date} 23:59:59"
    operations = get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE)

    # отфильтровываем только операции со статусом ОК
    operations = filter_by_state(operations)

    # отфильтровываем операции с нужными датами
    operations = filter_by_date(operations, start_date_operation, end_date_operation)

    # формируем json ответ
    print(get_views_json(operations))
