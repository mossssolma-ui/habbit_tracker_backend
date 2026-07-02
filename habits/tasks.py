from datetime import datetime

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_message_for_user():
    """Задача для напоминания о привычке пользователю в телеграм"""

    current_time = datetime.now().time()
    habits = Habit.objects.filter(
        is_pleasant_habit=False,
        user__tg_chat_id__isnull=False,
        time__hour=current_time.hour,
        time__minute=current_time.minute,
    )

    for habit in habits:
        message = f"Напоминание: {habit.action} в {habit.time.strftime('%H:%M')}, место: {habit.place}"
        if habit.reward:
            message += f"\nВознаграждение: {habit.reward}"
        if habit.related_habit:
            message += f"\nСвязанная привычка: {habit.related_habit.action}"
        send_telegram_message(habit.user.tg_chat_id, message)
