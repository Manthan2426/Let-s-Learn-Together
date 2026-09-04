from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Course, Review

# Demo reviewer accounts used to create multiple reviews per course.
REVIEWERS = ['admin', 'priya', 'rahul', 'sneha', 'arjun', 'meera', 'vikram', 'ananya']


class Command(BaseCommand):
    help = 'Populate courses with sample reviews from demo users.'

    def handle(self, *args, **options):
        # Ensure all demo reviewers exist.
        reviewers = []
        for username in REVIEWERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'pw-not-meaningful',
                },
            )
            if created:
                user.set_unusable_password()
                user.save()
            reviewers.append(user)

        reviews_data = {
            'javascript-from-zero-to-hero': [
                (5, 'Best intro to JS I have taken. The DOM section finally made it click for me.'),
                (4, 'Really well paced. Would love more on async/await though.'),
                (5, 'This is gold! My to-do app actually works!'),
                (4, 'Clear examples, solid instructor.'),
            ],
            'master-algebra-step-by-step': [
                (5, 'Explained so simply. I went from dreading algebra to solving them easily.'),
                (4, 'Great visuals. The word problems are challenging but fair.'),
                (5, 'The graphing section was my favourite.'),
            ],
            'sketching-for-absolute-beginners': [
                (5, 'I never thought I could draw. The shading lesson was a game-changer.'),
                (4, 'So relaxing and fun. Great for total beginners.'),
                (5, 'Perspective finally makes sense to me.'),
            ],
            'spanish-for-everyday-communication': [
                (5, 'Perfect for travel. I used these phrases in Mexico City!'),
                (4, 'Short lessons, easy to keep up daily.'),
            ],
            'personal-finance-for-beginners': [
                (5, 'Finally understand budgeting. The 50/30/20 rule is so practical.'),
                (4, 'Clear and no jargon. Wish it went deeper into investing.'),
                (5, 'Started my emergency fund right after lesson 3.'),
            ],
        }

        added = 0
        for slug, reviews in reviews_data.items():
            course = Course.objects.filter(slug=slug).first()
            if not course:
                self.stdout.write(self.style.WARNING(f'Skipped (no course): {slug}'))
                continue
            for i, (rating, comment) in enumerate(reviews):
                user = reviewers[i % len(reviewers)]
                _, created = Review.objects.get_or_create(
                    course=course,
                    user=user,
                    defaults={'rating': rating, 'comment': comment},
                )
                if created:
                    added += 1

        self.stdout.write(
            self.style.SUCCESS(f'Reviews: {Review.objects.count()} ({added} new)')
        )
