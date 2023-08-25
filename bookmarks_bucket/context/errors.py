"""
Сервис для хранения ссылок пользователей.
Кастомные обрабатываемые ошибки.
"""


class CustomError(Exception):
    """Кастомный класс ошибок"""


class NotFoundError(CustomError):
    """Указанный ресурс не найден"""


class ResourceGettingError(CustomError):
    """Не удаётся выполнить запрос"""


class ResourceFormatError(CustomError):
    """Ответ не соответствует ожидаемому формату"""


class ParsingError(CustomError):
    """Неверная структура ответа"""


class UnknownTypeError(CustomError):
    """Неизвестный тип страницы"""
