from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Модель пользователя для админки"""

    list_display = ("id", "email", "is_staff", "is_active", "is_superuser", "date_joined")
    list_filter = ("is_staff", "is_active", "is_superuser",)
    search_fields = ("email",)
    ordering = ("is_active", "-date_joined")
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        ("Изменить данные авторизации", {"fields": ("email", "password")}),
        ("Данные пользователя", {"fields": ("first_name", "last_name", "phone_number", "city", "avatar", "tg_chat_id")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Дата регистрации/входа", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        ("Создание пользователя", {
            "fields": ("email", "password1", "password2"),
        }),
    )
