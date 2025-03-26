import os

from src.logger import decorators_logger

PATH_TO_REPORTS_XLSX_FILE = os.path.join(os.path.dirname(__file__)[:-4], "reports")


def write_df_to_xlsx_file(file_name: str = "report.xlsx"):
    """
    Декоратор переводит результат выполнения функции из формата пандас дата фрейм в формат xlsx и
    записывает его в xlsx файл. Первоначально создан для функции spending_by_category модуля reports, которая
    возвращает данные по транзакциями за последние 3 месяца с указанной даты в указанной категории.
    Принимает filename, который определяет имя файла, в который будет записываться отчёт:
    По умолчанию имя задано, как report.xlsx, файл находится в папке reports в корне проекта.
    """
    def decorator(func):
        def wraper(*args, **kwargs):
            xls_report_file_name = os.path.join(PATH_TO_REPORTS_XLSX_FILE, file_name)
            # with open(xls_report_file_name, "w", encoding='utf-8') as file:
            result = func(*args, **kwargs)
            result.to_excel(xls_report_file_name, index=False)
            decorators_logger.info(
                f'xlsx файл с отчётом о работе функции {func.__name__} успешно записан в папку reports'
            )
            return result
        return wraper
    return decorator
