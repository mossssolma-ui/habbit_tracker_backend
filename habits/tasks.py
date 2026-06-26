from datetime import datetime

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_message_for_user():
    """Задача для напоминания о привычке пользователю в телеграм"""

    current_time = datetime.now().strftime("%H:%M")
    habits = Habit.objects.filter(is_pleasant_habit=False)

    for habit in habits:
        if current_time == habit.time.strftime("%H:%M"):
            if habit.user.tg_chat_id:
                message = f"Напоминание: {habit.action} " f"в {habit.time.strftime('%H:%M')}," f" место: {habit.place}"
                if habit.reward:
                    message += f"\nВознаграждение: {habit.reward}"
                if habit.related_habit:
                    message += f"\nСвязанная привычка: {habit.related_habit.action}"
                send_telegram_message(habit.user.tg_chat_id, message)
