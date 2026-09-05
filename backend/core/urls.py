from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import CategoryViewSet, CourseViewSet, test_api


router = DefaultRouter()

router.register("categories", CategoryViewSet)
router.register("courses", CourseViewSet)


urlpatterns = [
    path("test/", test_api),
]

urlpatterns += router.urls