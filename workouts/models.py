from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=100, default="General")
    difficulty = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField(blank=True)
    total_duration = models.IntegerField(default=0)
    exercises = models.ManyToManyField(Exercise, through="WorkoutEntry")

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class WorkoutEntry(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(validators=[MinValueValidator(1)])
    reps = models.IntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.exercise.name} ({self.workout.id})"
