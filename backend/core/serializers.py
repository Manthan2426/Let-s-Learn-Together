from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Category, Course, Enrollment, Lesson, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a user."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    # 8 to match Django's MinimumLengthValidator, so the client-side rule and
    # the server-side rule agree.
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate_email(self, value):
        # Django's default User model does NOT enforce this, so two accounts
        # could otherwise share an email address.
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'An account with this email already exists.'
            )
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )

        # Apply AUTH_PASSWORD_VALIDATORS, which were configured in settings
        # but never actually run on registration.
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': list(exc.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class CategorySerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'courses_count']

    def get_courses_count(self, obj):
        # Prefer the annotation added by CategoryViewSet (one query for the
        # whole list); fall back to a per-object count elsewhere.
        annotated = getattr(obj, 'published_courses_count', None)
        if annotated is not None:
            return annotated
        return obj.courses.filter(is_published=True).count()


class CourseListSerializer(serializers.ModelSerializer):
    """Compact course representation used in list views."""

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'category_slug',
            'icon',
            'level',
            'color',
            'lessons_count',
            'duration',
            'price',
            'old_price',
            'rating',
            'students_count',
            'instructor',
            'is_featured',
        ]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'duration', 'content', 'is_free_preview']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    course_slug = serializers.SlugField(source='course.slug', read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'user_id',
            'course_id',
            'course_slug',
            'rating',
            'comment',
            'created_at',
        ]

    def validate(self, attrs):
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You must be logged in to review.')

        # On an update the course is fixed; on a create it comes from course_id.
        course = attrs.get('course') or getattr(self.instance, 'course', None)

        if course is None:
            raise serializers.ValidationError({'course_id': 'This field is required.'})

        if not Enrollment.objects.filter(
            course=course, user=request.user
        ).exists():
            raise serializers.ValidationError(
                'Only learners enrolled in this course can review it.'
            )

        return attrs


class CourseDetailSerializer(serializers.ModelSerializer):
    """Full course representation including lessons and reviews."""

    category = CategorySerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'icon',
            'level',
            'color',
            'description',
            'lessons_count',
            'duration',
            'price',
            'old_price',
            'rating',
            'students_count',
            'instructor',
            'is_featured',
            'is_published',
            'lessons',
            'reviews',
            'created_at',
            'updated_at',
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_id', 'progress', 'enrolled_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError('You must be logged in to enrol.')
        return Enrollment.objects.create(user=request.user, **validated_data)
