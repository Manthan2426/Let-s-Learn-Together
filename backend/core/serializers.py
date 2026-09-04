from rest_framework import serializers

from .models import Category, Course, Enrollment, Lesson, Review


class CategorySerializer(serializers.ModelSerializer):
    courses_count = serializers.IntegerField(source='courses.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'courses_count']


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

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


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
