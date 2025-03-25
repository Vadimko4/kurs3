def log(filename: str = ''):
    """
    Декоратор логирует результаты выполнения функции, или возникшие ошибки.
    Принимает filename, который определяет,куда будут записываться логи (в файл или в консоль):
    если filename задан, логи записываются в указанный файл; нет - логи выводятся в консоль.
    Логирование включает: имя функции и  результат выполнения при успешной операции, либо
    имя функции, тип возникшей ошибки и входные параметры, если выполнение функции привело к ошибке;
    """
    def decorator(func):
        def wraper(*args, **kwargs):
            if filename:
                with open(filename, "a", encoding='utf-8') as file:
                    try:
                        result = func(*args, **kwargs)
                        file.write(f"{func.__name__} ok\n")
                        return result
                    except Exception as e:
                        file.write(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}\n")
                        raise Exception(e)
            else:
                try:
                    result = func(*args, **kwargs)
                    print(f"{func.__name__} ok")
                    return result
                except Exception as e:
                    print(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
                    raise Exception(e)
        return wraper
    return decorator
