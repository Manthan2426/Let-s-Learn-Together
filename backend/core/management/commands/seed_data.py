from django.core.management.base import BaseCommand

from core.models import Category, Course


class Command(BaseCommand):
    help = 'Populate the database with starter categories and courses.'

    def handle(self, *args, **options):
        # ---- Categories -------------------------------------------------
        categories = {
            'Coding & Tech': '💻',
            'Math & Science': '📐',
            'Art & Design': '🎨',
            'Language': '🗣️',
            'Business': '💼',
            'Personal Growth': '🌱',
        }
        cat_objs = {}
        for name, icon in categories.items():
            obj, _ = Category.objects.update_or_create(
                name=name, defaults={'icon': icon}
            )
            cat_objs[name] = obj
        self.stdout.write(self.style.SUCCESS(f'Categories: {Category.objects.count()}'))

        # ---- Courses (match the existing front-end cards) ----------------
        courses = [
            {
                'title': 'JavaScript from Zero to Hero',
                'category': 'Coding & Tech',
                'icon': '💻',
                'level': Course.Level.BEGINNER,
                'color': Course.Color.PURPLE,
                'lessons_count': 48,
                'duration': '12h 30m',
                'price': 1299,
                'old_price': 1999,
                'rating': 4.90,
                'students_count': 12400,
                'instructor': 'Aarav Mehra',
                'description': (
                    'Go from writing your first script to building real '
                    'interactive web apps. Variables, functions, the DOM, '
                    'async JavaScript and a final project.'
                ),
            },
            {
                'title': 'Master Algebra — Step by Step',
                'category': 'Math & Science',
                'icon': '📐',
                'level': Course.Level.BEGINNER,
                'color': Course.Color.ORANGE,
                'lessons_count': 36,
                'duration': '9h 15m',
                'price': 999,
                'old_price': 1499,
                'rating': 4.80,
                'students_count': 8700,
                'instructor': 'Dr. Ritu Sharma',
                'description': (
                    'A friendly, visual approach to algebra: equations, '
                    'functions, inequalities and real-world word problems.'
                ),
            },
            {
                'title': 'Sketching for Absolute Beginners',
                'category': 'Art & Design',
                'icon': '🎨',
                'level': Course.Level.BEGINNER,
                'color': Course.Color.PINK,
                'lessons_count': 24,
                'duration': '6h 20m',
                'price': 799,
                'old_price': 1199,
                'rating': 4.90,
                'students_count': 6200,
                'instructor': 'Elena Vargas',
                'description': (
                    'Learn to see like an artist: lines, shapes, shading and '
                    'perspective with just a pencil and sketchbook.'
                ),
            },
            {
                'title': 'Spanish for Everyday Communication',
                'category': 'Language',
                'icon': '🗣️',
                'level': Course.Level.BEGINNER,
                'color': Course.Color.TEAL,
                'lessons_count': 40,
                'duration': '10h 00m',
                'price': 1099,
                'old_price': 1599,
                'rating': 4.70,
                'students_count': 5400,
                'instructor': 'Diego Fernández',
                'description': (
                    'Speak useful Spanish for travel, work and friends with '
                    'short conversational lessons and daily practice.'
                ),
            },
            {
                'title': 'Personal Finance for Beginners',
                'category': 'Business',
                'icon': '💼',
                'level': Course.Level.BEGINNER,
                'color': Course.Color.GREEN,
                'lessons_count': 30,
                'duration': '7h 45m',
                'price': 1499,
                'old_price': 2199,
                'rating': 4.80,
                'students_count': 9100,
                'instructor': 'Kavita Nair',
                'description': (
                    'Budgeting, saving, investing and credit — build a simple '
                    'money system that works for you.'
                ),
            },
        ]

        created = 0
        for data in courses:
            cat = cat_objs[data['category']]
            slug = data['title'].lower().replace(' — ', '-').replace(' ', '-')
            obj, was_created = Course.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': data['title'],
                    'category': cat,
                    'icon': data['icon'],
                    'level': data['level'],
                    'color': data['color'],
                    'lessons_count': data['lessons_count'],
                    'duration': data['duration'],
                    'price': data['price'],
                    'old_price': data['old_price'],
                    'rating': data['rating'],
                    'students_count': data['students_count'],
                    'instructor': data['instructor'],
                    'description': data['description'],
                    'is_featured': True,
                    'is_published': True,
                },
            )
            created += 1 if was_created else 0
        self.stdout.write(
            self.style.SUCCESS(
                f'Courses: {Course.objects.count()} ({created} new)'
            )
        )
        self.stdout.write(self.style.SUCCESS('Seed data ready ✔'))
