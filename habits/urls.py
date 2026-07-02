from django.urls import path
from rest_framework import routers

from habits import views
from habits.apps import HabitsConfig
from habits.views import PublicHabitListAPIView

app_name = HabitsConfig.name

router = routers.DefaultRouter()
router.register(r"habits", views.HabitViewSet, basename="habits")

urlpatterns = [
    path("habits/public/", PublicHabitListAPIView.as_view(), name="public-habits"),
] + router.urls
