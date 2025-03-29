import os

import requests
from dotenv import load_dotenv

# from src.logger import external_api_logger

# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменных GITHUB_TOKEN из .env-файла
currency_api_key = os.getenv('CURRENCY_API_KEY')
stocks_api_key = os.getenv('STOCKS_API_KEY')


def get_rub_transaction_amount(amount: float, currency: str) -> float:
    """
    Функция переводит сумму amount в валюте currency - в рубли по актуальному курсу, тип данных — float.
    для получения текущего курса валют и конвертации происходит обращение к внешнему API
    """

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {
        "apikey": currency_api_key
    }
    payload = {
        "amount": abs(amount),
        "from": currency,
        "to": "RUB"
    }
    response = requests.get(url, headers=headers, params=payload)
    # status_code = response.status_code

    sign = (-1) ** (amount < 0)
    result_amount = response.json().get("result") * sign

    return round(result_amount, 2)


def get_currency_too_rub_rate(currency: str) -> float:
    """
    Функция возвращает актуальный курс указанной валюты к рублю
    """
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {
        "apikey": currency_api_key
    }
    payload = {
        "amount": 1.00,
        "from": currency,
        "to": "RUB"
    }
    response = requests.get(url, headers=headers, params=payload)
    # res = response.json()
    # print(res)
    # if "exceeded" in res.get("message"):
    #     external_api_logger.error(f'При обращении к API exchangerates_data возникла ошибка. Слишком много обращений')
    #     raise ValueError('Количество обращений к API превышено! Вероятно, нужно обновить API-key')

    result_amount = response.json().get("info").get("rate")
    # status_code = response.status_code
    return round(result_amount, 2)


def get_stock_rub_price(stock: str) -> float:
    """
    Функция возвращает актуальную стоимость указанной акции в рублях
    """
    url = f"https://api.marketstack.com/v1/eod?access_key={stocks_api_key}"
    querystring = {"symbols": stock}
    response = requests.get(url, params=querystring)
    # status_code = response.status_code

    #  вытаскиваем из ответа json цену на момент открытия в ближайший прошедший торговый день
    #  и из USD конвертим в рубли
    result_amount = get_rub_transaction_amount(response.json().get('data')[0].get('open'), "USD")

    return round(result_amount, 2)


if __name__ == '__main__':
    # print(get_rub_transaction_amount({
    #             'Дата операции': '26.07.2021 20:35:57', 'Дата платежа': '26.07.2021',
    #             'Номер карты': '*4556', 'Статус': 'OK', 'Сумма операции': -135.0,
    #             'Валюта операции': 'USD', 'Сумма платежа': -250.0,
    #             'Валюта платежа': 'RUB', 'Кэшбэк': None, 'Категория': 'Связь',
    #             'MCC': 4814.0, 'Описание': 'МТС', 'Бонусы (включая кэшбэк)': 0,
    #             'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 250.0
    #         }))
    print(get_currency_too_rub_rate('USD'))
    # print(get_stock_rub_price('TSLA'))
