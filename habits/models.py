from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="habits",
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        help_text="Создатель привычки"
    )
    place = models.CharField(max_length=300, verbose_name="Место выполнения привычки",
                             help_text="Место, в котором необходимо выполнять привычку")
    time = models.TimeField(verbose_name="Время выполнения привычки",
                            help_text="Время, когда необходимо выполнять привычку")
    action = models.CharField(max_length=300, verbose_name="Действие привычки",
                              help_text="Действие, которое представляет собой привычка")
    is_pleasant_habit = models.BooleanField(default=False, verbose_name="Приятная привычка",
                                            help_text="Привычка, которую можно привязать к выполнению полезной привычки")
    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="related_habits", blank=True, null=True,
                                      verbose_name="Связанная привычка",
                                      help_text="Связанную привычку можно не указывать")
    frequency = models.PositiveIntegerField(default=1, verbose_name="Частота привычки",
                                            help_text="Укажите периодичность выполнения привычки в днях")
    reward = models.CharField(max_length=300, blank=True, null=True, verbose_name="Вознаграждение",
                              help_text="Чем пользователь должен себя вознаградить после выполнения")

    time_to_complete = models.PositiveIntegerField(verbose_name="Время выполнение в секундах(не больше 120 с)",
                                                   default=120, help_text="Укажите время выполнения привычки")
    is_public = models.BooleanField(default=False, verbose_name="Публичность привычки", help_text="Указать публичность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['-created_at']
