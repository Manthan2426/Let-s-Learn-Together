from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Course, Lesson
from .serializers import (
    CategorySerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    LessonSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve published courses.

    ?featured=true        -> only featured courses
    ?category=coding-tech -> filter by category slug
    ?search=javascript    -> full-text-ish search over title/instructor
    """

    queryset = Course.objects.filter(is_published=True).select_related('category')
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        featured = self.request.query_params.get('featured')
        if featured in ('true', '1'):
            qs = qs.filter(is_featured=True)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(title__icontains=search).order_by('-rating')[:20]
        return qs


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve lessons (optionally scoped to a course slug)."""

    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Lesson.objects.select_related('course')
        course = self.request.query_params.get('course')
        if course:
            qs = qs.filter(course__slug=course)
        return qs


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'service': 'let-s-learn-together-api'})
