from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import CustomPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """
    CRUD для управления привычками
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = CustomPaginator

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "is_public",
        "place",
    )

    ordering_fields = ("created_at",)

    def get_queryset(self):
        """Возвращает привычки текущего пользователя"""
        if self.request.user.is_anonymous:
            return Habit.objects.none()

        user = self.request.user
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """Привычка при создании привязывается к текущему пользователю"""
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        """Передача request в контекст сериализатора"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_permissions(self):
        """Назначение прав доступа при различных действиях"""
        if self.action in ["list", "create", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Получить список своих привычек с пагинацией и статистикой",
        responses={
            200: openapi.Response(
                description="Список привычек",
                examples={
                    "application/json": {
                        "count": 5,
                        "next": "http://localhost:8000/api/habits/?page=2",
                        "previous": None,
                        "total_count": 10,
                        "public_count": 3,
                        "private_count": 7,
                        "pleasant_count": 2,
                        "results": [
                            {"id": 1, "place": "Дом", "time": "08:00:00", "action": "Зарядка", "is_public": True}
                        ],
                    }
                },
            )
        },
    )
    def list(self, request, *args, **kwargs):
        """Переопределение list для возврата статистики"""
        queryset = self.filter_queryset(self.get_queryset())

        total_count = queryset.count()
        public_count = queryset.filter(is_public=True).count()
        private_count = queryset.filter(is_public=False).count()
        pleasant_count = queryset.filter(is_pleasant_habit=True).count()

        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return Response(
                {
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "total_count": total_count,
                    "public_count": public_count,
                    "private_count": private_count,
                    "pleasant_count": pleasant_count,
                    "results": serializer.data,
                }
            )


class PublicHabitListAPIView(generics.ListAPIView):
    """Вывод только публичных привычек"""

    serializer_class = HabitSerializer
    pagination_class = CustomPaginator
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список публичных привычек (доступно без авторизации)",
        responses={
            200: HabitSerializer(many=True),
        },
    )
    def get_queryset(self):
        """Возвращает только публичные привычки"""
        return Habit.objects.filter(is_public=True)
