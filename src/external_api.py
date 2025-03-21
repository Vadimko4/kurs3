import os

import requests
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменной GITHUB_TOKEN из .env-файла
api_key = os.getenv('API_KEY')


def get_rub_transaction_amount(transaction: dict) -> float:
    """
    Функция возвращает сумму транзакции в рублях, тип данных — float.
    Если транзакция была в USD или EUR, происходит обращение к внешнему API
    для получения текущего курса валют и конвертации суммы операции в рубли
    """
    if "Сумма операции" not in transaction or "Валюта операции" not in transaction:
        raise ValueError('Неверные данные о транзакции')

    if transaction["Валюта операции"] == "RUB":
        result_amount = transaction["Сумма операции"]
    else:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {
            "apikey": api_key
        }
        payload = {
            "amount": abs(transaction.get("Сумма операции")),
            "from": transaction.get("Валюта операции"),
            "to": "RUB"
        }
        response = requests.get(url, headers=headers, params=payload)

        sign = (-1) ** (transaction.get("Сумма операции") < 0)
        result_amount = response.json().get("result") * sign
        # status_code = response.status_code

    return round(result_amount, 2)


if __name__ == '__main__':
    print(get_rub_transaction_amount({
                'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
                'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -135.0,
                'Валюта операции': 'TRY', 'Сумма платежа': -250.0,
                'Валюта платежа': 'RUB', 'Кэшбэк': None, 'Категория': 'Связь',
                'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
                'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
            }))
