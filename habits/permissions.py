from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsOwner(IsAuthenticated):
    """Проверка, что юзер является владельцем объекта"""

    message = "Вы не являетесь владельцем этой привычки"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
