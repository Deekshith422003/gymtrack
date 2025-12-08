from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet, ExerciseViewSet

router = DefaultRouter()
router.register("workouts", WorkoutViewSet, basename="workouts")
router.register("exercises", ExerciseViewSet, basename="exercises")

urlpatterns = router.urls
