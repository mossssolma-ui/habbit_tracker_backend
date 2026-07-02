class TGServiceError(Exception):
    """Базовое исключение ошибок в Telegram сервисе"""

    ...


class FailedToConnect(TGServiceError):
    """Ошибка подключения к Telegram API"""

    ...
