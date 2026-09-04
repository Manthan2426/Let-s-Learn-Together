from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('courses', views.CourseViewSet, basename='course')
router.register('lessons', views.LessonViewSet, basename='lesson')
router.register('enrollments', views.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health'),
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', views.me, name='auth-me'),
]
