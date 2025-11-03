from django.contrib import admin
from .models import Workout, Exercise

# Optional: Customize how models appear in the admin interface

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_duration', 'notes')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'notes')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'difficulty')
    list_filter = ('muscle_group', 'difficulty')
    search_fields = ('name',)

