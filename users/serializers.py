from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        model = CustomUser
        fields = ("id", "email", "phone_number", "city", "avatar", "password", "is_superuser", "is_staff", "is_active")
        extra_kwargs = {
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
