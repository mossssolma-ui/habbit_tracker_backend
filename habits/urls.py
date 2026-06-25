
from django.urls import path, include

from habits.apps import HabitsConfig

app_name = HabitsConfig.name
urlpatterns = [
    # path('', include('habits.urls', namespace='habits')),
]
