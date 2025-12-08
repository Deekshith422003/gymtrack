from django.utils.html import escape
from rest_framework import serializers
from .models import Workout, Exercise, WorkoutEntry


def sanitize_text(value):
    if "<script" in value.lower():
        raise serializers.ValidationError("Javascript not allowed.")
    return escape(value)


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name", "muscle_group", "difficulty"]


class WorkoutEntrySerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutEntry
        fields = ["exercise", "sets", "reps", "weight"]


class WorkoutSerializer(serializers.ModelSerializer):
    entries = WorkoutEntrySerializer(source="workoutentry_set", many=True, read_only=True)

    # simple form fields
    exercise_name = serializers.CharField(write_only=True)
    sets = serializers.IntegerField(write_only=True)
    reps = serializers.IntegerField(write_only=True)

    class Meta:
        model = Workout
        fields = [
            "id",
            "date",
            "notes",
            "total_duration",
            "entries",
            "exercise_name",
            "sets",
            "reps",
        ]

    def create(self, validated_data):
        exercise_name = sanitize_text(validated_data.pop("exercise_name"))
        sets = validated_data.pop("sets")
        reps = validated_data.pop("reps")
        user = validated_data.pop("user")

        workout = Workout.objects.create(user=user, **validated_data)

        exercise, _ = Exercise.objects.get_or_create(
            name=exercise_name, defaults={"muscle_group": "General", "difficulty": 1}
        )

        WorkoutEntry.objects.create(
            workout=workout,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weight=0.0,
        )
        return workout
