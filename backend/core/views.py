from rest_framework import viewsets
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer
from django.http import JsonResponse


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

def test_api(request):
      return JsonResponse({
        "message": "Backend connected successfully!",
        "status": "success"
    })