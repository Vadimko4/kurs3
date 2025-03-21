from unittest.mock import patch
from src.utils import get_greeting, get_operations_from_xlsx, PATH_TO_OPERATIONS_XLSX_FILE


@patch("src.utils.datetime.datetime")
def test_get_greeting(mock_datetime):
    mock_datetime.now.return_value.hour = 10
    assert get_greeting() == "Доброе утро!"
    mock_datetime.now.return_value.hour = 15
    assert get_greeting() == "Добрый день!"
    mock_datetime.now.return_value.hour = 20
    assert get_greeting() == "Добрый вечер!"
    mock_datetime.now.return_value.hour = 1
    assert get_greeting() == "Доброй ночи!"


@patch('pandas.read_excel')
def test_get_operations_from_xlsx(mock_get):
    mock_get.return_value.to_dict.return_value = []
    assert get_operations_from_xlsx(PATH_TO_OPERATIONS_XLSX_FILE) == []
    mock_get.assert_called_with(PATH_TO_OPERATIONS_XLSX_FILE)
