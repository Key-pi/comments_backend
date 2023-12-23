from apps.comments.models import Comment

from django.core.management.base import BaseCommand

from faker import Faker




class Command(BaseCommand):
    help = "Create random boards" # noqa A003

    def add_arguments(self, parser):
        parser.add_argument("total", type=int, choices=range(1, 1000), help='Number of users to create')

    def handle(self, *args, **options):
        fake = Faker()
        total = options['total']
        obj = [
            Comment(
                email=fake.email(),
                text=fake.text(),
                parent_comment=None,

            )
            for _ in range(total)
        ]

        Comment.objects.bulk_create(obj)
        print("Comments Created!") # noqa T001