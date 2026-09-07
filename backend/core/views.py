from django.contrib.auth import get_user_model
from django.db.models import Count, F, Q

from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Course, Enrollment, Lesson, Review
from .serializers import (
    CategorySerializer,
    CourseDetailSerializer,
    CourseListSerializer,
    EnrollmentSerializer,
    LessonSerializer,
    RegisterSerializer,
    ReviewSerializer,
    UserSerializer,
)


User = get_user_model()


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """
    Create a new user account.
    Returns JWT tokens so the frontend can log in immediately.
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    # Uses the 'auth' rate defined in settings.DEFAULT_THROTTLE_RATES so
    # sign-up cannot be hammered from a single address.
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

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

    return Response(
        UserSerializer(request.user).data
    )


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    List the logged-in user's enrollments,
    or enroll in a course with POST.
    """

    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return (
            Enrollment.objects
            .filter(user=self.request.user)
            .select_related('course')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = serializer.validated_data['course']

        obj, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )

        if created:
            # F() keeps the counter correct when two learners enroll at once.
            Course.objects.filter(pk=course.pk).update(
                students_count=F('students_count') + 1
            )

        out = EnrollmentSerializer(
            obj,
            context={'request': request}
        )

        return Response(
            out.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )

    def perform_destroy(self, instance):
        """Un-enrolling must give the seat back to students_count."""

        course_pk = instance.course_id
        instance.delete()

        Course.objects.filter(
            pk=course_pk,
            students_count__gt=0
        ).update(
            students_count=F('students_count') - 1
        )


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve categories."""

    queryset = Category.objects.annotate(
        published_courses_count=Count(
            'courses',
            filter=Q(courses__is_published=True),
        )
    )
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve published courses.

    ?featured=true
        -> only featured courses

    ?category=coding-tech
        -> filter by category slug

    ?search=javascript
        -> search courses by title
    """

    queryset = (
        Course.objects
        .filter(is_published=True)
        .select_related('category')
    )

    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer

        return CourseListSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == 'retrieve':
            # The detail serializer nests lessons and reviews; prefetch them
            # so one course page is 3 queries instead of 1 + 2N.
            return qs.prefetch_related('lessons', 'reviews__user')

        featured = self.request.query_params.get('featured')

        if featured in ('true', '1'):
            qs = qs.filter(is_featured=True)

        category = self.request.query_params.get('category')

        if category:
            qs = qs.filter(category__slug=category)

        search = self.request.query_params.get('search')

        if search:
            # NOTE: the slice must stay last and must never run for `retrieve`
            # — filtering an already-sliced queryset raises
            # "Cannot filter a query once a slice has been taken."
            qs = qs.filter(
                title__icontains=search
            ).order_by('-rating')[:20]

        return qs


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve lessons, optionally scoped to a course."""

    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Lesson.objects.select_related('course')

        course = self.request.query_params.get('course')

        if course:
            qs = qs.filter(course__slug=course)

        return qs


# ---------------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------------

class IsReviewAuthorOrReadOnly(BasePermission):
    """Anyone may read a review; only its author may change or delete it."""

    message = 'You can only edit your own review.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user_id == request.user.id


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Read, write and remove course reviews.

    ?course=javascript-from-zero-to-hero
        -> only reviews for that course

    ?mine=true
        -> only the signed-in learner's own reviews

    Posting twice for the same course updates the existing review instead of
    failing on the (course, user) uniqueness constraint.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.select_related('user', 'course')

        course = self.request.query_params.get('course')

        if course:
            qs = qs.filter(course__slug=course)

        mine = self.request.query_params.get('mine')

        if mine in ('true', '1') and self.request.user.is_authenticated:
            qs = qs.filter(user=self.request.user)

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = serializer.validated_data['course']

        review, created = Review.objects.update_or_create(
            course=course,
            user=request.user,
            defaults={
                'rating': serializer.validated_data['rating'],
                'comment': serializer.validated_data.get('comment', ''),
            },
        )

        course.recalculate_rating()

        out = self.get_serializer(review)

        return Response(
            out.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )

    def perform_update(self, serializer):
        review = serializer.save(user=self.request.user)
        review.course.recalculate_rating()

    def perform_destroy(self, instance):
        course = instance.course
        instance.delete()
        course.recalculate_rating()


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@api_view(['GET'])
def health_check(request):
    return Response(
        {
            'status': 'ok',
            'service': 'let-s-learn-together-api'
        }
    )


# ---------------------------------------------------------------------------
# Test API
# ---------------------------------------------------------------------------

@api_view(['GET'])
def test_api(request):
    return Response(
        {
            'message': 'Backend connected successfully!',
            'status': 'success'
        }
    )