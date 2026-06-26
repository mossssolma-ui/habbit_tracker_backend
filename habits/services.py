import requests

from config.settings import TELEGRAM_URL, TG_API_KEY
from habits.exceptions import FailedToConnect


def send_telegram_message(chat_id: str, message: str) -> None:
    """Функция отправки сообщения пользователю о привычке в телеграм"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    try:
        response = requests.get(f"{TELEGRAM_URL}{TG_API_KEY}/sendMessage", params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise FailedToConnect(f"Ошибка подключения к ТГ: {e}") from e
