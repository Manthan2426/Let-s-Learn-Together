from django.contrib import admin

from .models import Category, Course, Enrollment, Lesson, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'description', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'level',
        'price',
        'rating',
        'students_count',
        'is_featured',
        'is_published',
    )
    list_filter = ('category', 'level', 'color', 'is_featured', 'is_published')
    search_fields = ('title', 'instructor')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_published')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration', 'is_free_preview')
    list_filter = ('course', 'is_free_preview')
    ordering = ('course', 'order')
    search_fields = ('title',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'progress')
    list_filter = ('course',)
    search_fields = ('user__username', 'course__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'course')
    search_fields = ('user__username', 'course__title', 'comment')
