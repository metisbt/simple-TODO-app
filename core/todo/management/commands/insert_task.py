from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from accounts.models import User, Profile
from todo.models import Task
import random
from datetime import datetime


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        # create fake user and profile
        user = User.objects.create_user(email=self.fake.email(), password='Test@123456')
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(nb_sentences=5)
        profile.save()


        for _ in range(5):
            Task.objects.create(
                author = profile,
                title = self.fake.paragraph(nb_sentences=1),
                complete = True,
                updated_date = datetime.now()
            )