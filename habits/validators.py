from rest_framework import serializers


def validate_reward_and_related_habit(reward, related_habit):
    """
    Валидатор исключающий одновременный выбор
    связанной привычки и указания вознаграждения
    """
    if reward and related_habit:
        raise serializers.ValidationError("Заполните только одно из двух полей: 'Награда' или 'Связанная привычка'")


def validate_duration(value):
    """
    Валидатор проверяющий, что время выполения не более 120 секунд
    """
    if value is None:
        raise serializers.ValidationError("Укажите продолжительность привычки")
    if value > 120:
        raise serializers.ValidationError("Продолжительность привычки должно быть не более 120 секунд")


def validate_related_habit_pleasant(related_habit):
    """
    Валидатор проверяющий, что в связанные привычки могут
    попадать только привычки с признаком приятной привычки.
    """
    if related_habit and not related_habit.is_pleasant_habit:
        raise serializers.ValidationError("Связанная привычка должна быть приятной")


def validate_pleasant_no_reward_or_related(is_pleasant_habit, reward, related_habit):
    """
    Валидатор проверки, что у приятной привычки
    не может быть вознаграждения или связанной привычки
    """
    if is_pleasant_habit and (reward or related_habit):
        raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")


def validate_frequency(value):
    """
    Валидатор проверяющий, что частота выполнения привычки от 1 до 7 дней
    """
    if value is None:
        raise serializers.ValidationError("Укажите частоту выполнения привычки")
    if value < 1 or value > 7:
        raise serializers.ValidationError("Частота привычки должна быть от 1 до 7 дней")
