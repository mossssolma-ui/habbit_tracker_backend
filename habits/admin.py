from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "action", "place", "time", "is_public", "frequency", "time_to_complete")
    list_filter = ("is_public", "is_pleasant_habit", "frequency", "created_at")
    search_fields = ("action", "place", "user__email")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основная информация", {"fields": ("user", "place", "time", "action")}),
        (
            "Настройки привычки",
            {"fields": ("is_pleasant_habit", "related_habit", "frequency", "reward", "time_to_complete")},
        ),
        ("Публичность", {"fields": ("is_public",)}),
        ("Дата создания/изменения", {"fields": ("created_at", "updated_at")}),
    )
