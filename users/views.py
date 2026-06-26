from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация пользователя"""

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация пользователя",
        request_body=CustomUserSerializer,
        responses={
            201: CustomUserSerializer,
            409: "Пользователь существует",
        },
    )
    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            return Response({"message": "Пользователь существует"}, status=status.HTTP_409_CONFLICT)
        return super().create(request, *args, **kwargs)


class UserListAPIView(generics.ListAPIView):
    """Просмотр всех пользователей (для суперюзера)"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        operation_description="Просмотр всех пользователей (для суперюзера)",
        responses={200: CustomUserSerializer(many=True), 403: "Доступ запрещен (требуются права суперюзера)"},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр/Обновление/Удаление пользователя"""

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    @swagger_auto_schema(
        operation_description="Получить информацию о пользователе по ID",
        responses={200: CustomUserSerializer, 404: "Пользователь не найден"},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить пользователя",
        request_body=CustomUserSerializer,
        responses={
            200: CustomUserSerializer,
            400: "Ошибка валидации",
            403: "Доступ запрещен",
            404: "Пользователь не найден",
        },
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить пользователя",
        request_body=CustomUserSerializer,
        responses={
            200: CustomUserSerializer,
            400: "Ошибка валидации",
            403: "Доступ запрещен",
            404: "Пользователь не найден",
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить пользователя (только суперюзер)",
        responses={204: "Пользователь успешно удален", 403: "Доступ запрещен", 404: "Пользователь не найден"},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
