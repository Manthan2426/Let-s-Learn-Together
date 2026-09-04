from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """A top-level subject area, e.g. 'Coding & Tech', 'Art & Design'."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=10, blank=True, default='📚')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    """A course that learners can enrol in."""

    class Level(models.TextChoices):
        BEGINNER = 'Beginner', 'Beginner'
        INTERMEDIATE = 'Intermediate', 'Intermediate'
        ADVANCED = 'Advanced', 'Advanced'

    class Color(models.TextChoices):
        PURPLE = 'purple', 'Purple'
        ORANGE = 'orange', 'Orange'
        PINK = 'pink', 'Pink'
        TEAL = 'teal', 'Teal'
        BLUE = 'blue', 'Blue'
        GREEN = 'green', 'Green'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category, related_name='courses', on_delete=models.PROTECT
    )
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True, default='📘')

    # Level + visual accent, matching the existing front-end cards.
    level = models.CharField(
        max_length=20, choices=Level.choices, default=Level.BEGINNER
    )
    color = models.CharField(
        max_length=10, choices=Color.choices, default=Color.PURPLE
    )

    # Content metadata (displayed on the card as '48 lessons', '12h 30m').
    lessons_count = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=20, blank=True, default='0h 0m')

    # Pricing (in rupees) and social proof.
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    old_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    students_count = models.IntegerField(default=0)

    # The person leading the course (stored as text for now; can be a FK later).
    instructor = models.CharField(max_length=120, blank=True, default='')

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-rating', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def preview_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})


class Lesson(models.Model):
    """A single lesson inside a course."""

    course = models.ForeignKey(
        Course, related_name='lessons', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    duration = models.CharField(max_length=20, blank=True, default='10m')
    content = models.TextField(blank=True, help_text='Markdown or plain text body.')
    is_free_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.course.title} — {self.title}'


class Enrollment(models.Model):
    """A learner's membership in a course."""

    course = models.ForeignKey(
        Course, related_name='enrollments', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0, help_text='0.0 to 1.0')

    class Meta:
        unique_together = ('course', 'user')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.user} → {self.course}'


class Review(models.Model):
    """A rating + comment left by a learner on a course."""

    course = models.ForeignKey(
        Course, related_name='reviews', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        default=5, help_text='1 to 5'
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('course', 'user')

    def __str__(self):
        return f'{self.user} → {self.course} ({self.rating}★)'
