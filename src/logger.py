import logging
import os

PATH_TO_LOGS_DIR = os.path.join(os.path.dirname(__file__)[:-4], "logs")
APPLICATION_LOG_FILE_NAME = os.path.join(PATH_TO_LOGS_DIR, "application.log")


# Основная конфигурация logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=APPLICATION_LOG_FILE_NAME,  # Запись логов в файл
                    encoding='utf-8',
                    filemode='w')  # Перезапись файла при каждом запуске


# Создаем логеры для различных компонентов программы
utils_logger = logging.getLogger('utils')
views_logger = logging.getLogger('views')
external_api_logger = logging.getLogger('external_api')
services_logger = logging.getLogger('services')
reports_logger = logging.getLogger('reports')
decorators_logger = logging.getLogger('decorators')
