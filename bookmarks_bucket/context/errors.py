"""
Сервис для хранения ссылок пользователей.
Кастомные обрабатываемые ошибки.
"""


class NotFoundError(Exception):
    """Указанный ресурс не найден"""


class ResourceGettingError(Exception):
    """Не удаётся выполнить запрос"""


class ResourceFormatError(Exception):
    """Ответ не соответствует ожидаемому формату"""


class ParsingError(Exception):
    """Неверная структура ответа"""


class UnknownTypeError(Exception):
    """Неизвестный тип страницы"""
