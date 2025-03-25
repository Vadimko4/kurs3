from src.services import get_categories


def test_get_categories(test_rub_operation_list):
    assert (get_categories(test_rub_operation_list) ==
            ['Переводы', 'Пополнения', 'Связь', 'Транспорт', 'Фастфуд'])
    assert get_categories([]) == []
