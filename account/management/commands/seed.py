from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from random import choice
from string import digits
import pytz
import datetime


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def post(self, *args, **kwargs):
        total = kwargs['total']
        unaware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0)
        now_aware = unaware.replace(tzinfo=pytz.UTC)
        for i in range(total):
            user = User.objects.create(
                username='W0' + ''.join(choice(digits) for j in range(7)),
                email='anup@mail.com',
                password='123456',
                tz=now_aware
            )
            user.save()