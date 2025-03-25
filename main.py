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
    req_date = foolproof_user_date_input()

    print('\nПрограмма: Идёт формирование ответа на ваш запрос...')
    # формируем json ответ
    json_answer = get_views_json(req_date)
    print(json_answer)
