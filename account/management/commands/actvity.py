from django.contrib.auth.models import ActivityPeriod, User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from datetime import datetime
from django.utils import formats

class Command(BaseCommand):
    help = 'Create random users'

    def post(self, *args, **kwargs):
        user = User.objects.values()
        for i in user:
            act = ActivityPeriod.objects.create(
                start_time=datetime.now(),
                end_time=datetime.now(),
                user=i['id']
            )
            act.save()