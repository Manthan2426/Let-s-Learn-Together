from django.core.management.base import BaseCommand

from core.models import Course, Lesson


class Command(BaseCommand):
    help = 'Populate courses with a handful of sample lessons.'

    def handle(self, *args, **options):
        lessons_data = {
            'javascript-from-zero-to-hero': [
                ('Welcome & Course Tour', '06m', True),
                ('Setting Up Your Editor', '09m', True),
                ('Variables & Data Types', '14m', False),
                ('Functions & Scope', '18m', False),
                ('The DOM & Events', '22m', False),
                ('Build a To-Do App', '28m', False),
            ],
            'master-algebra-step-by-step': [
                ('Why Algebra Matters', '07m', True),
                ('Order of Operations', '12m', False),
                ('Solving Linear Equations', '16m', False),
                ('Graphing Lines', '15m', False),
            ],
            'sketching-for-absolute-beginners': [
                ('Your Materials', '05m', True),
                ('Lines & Contours', '11m', False),
                ('Shading Basics', '13m', False),
                ('Perspective 101', '17m', False),
            ],
            'spanish-for-everyday-communication': [
                ('Greetings & Introductions', '08m', True),
                ('Numbers & Dates', '10m', False),
                ('Ordering Food', '12m', False),
                ('Small Talk', '14m', False),
            ],
            'personal-finance-for-beginners': [
                ('Money Mindset', '06m', True),
                ('The 50/30/20 Budget', '12m', False),
                ('Build an Emergency Fund', '10m', False),
                ('Intro to Investing', '20m', False),
            ],
        }

        added = 0
        for slug, lessons in lessons_data.items():
            course = Course.objects.filter(slug=slug).first()
            if not course:
                self.stdout.write(self.style.WARNING(f'Skipped (no course): {slug}'))
                continue
            for order, (title, dur, free) in enumerate(lessons, start=1):
                _, created = Lesson.objects.get_or_create(
                    course=course,
                    title=title,
                    defaults={'order': order, 'duration': dur, 'is_free_preview': free},
                )
                if created:
                    added += 1
            # Keep a sensible snapshot of lesson count on the course.
            course.lessons_count = course.lessons.count()
            course.save(update_fields=['lessons_count'])

        self.stdout.write(
            self.style.SUCCESS(f'Lessons: {Lesson.objects.count()} ({added} new)')
        )
