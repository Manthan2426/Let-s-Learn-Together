from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Course, Enrollment, Lesson
from .serializers import (
    CategorySerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    EnrollmentSerializer,
    LessonSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """Create a new user account. Returns JWT tokens so the frontend can log in immediately."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Return the currently authenticated user."""
    return Response(UserSerializer(request.user).data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """List the logged-in user's enrollments, or enrol in a course with POST."""

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data['course']
        obj, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            course.students_count += 1
            course.save(update_fields=['students_count'])
        out = EnrollmentSerializer(obj, context={'request': request})
        return Response(out.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

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
