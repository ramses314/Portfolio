from django.core.management.base import BaseCommand

from applications.users.models import CustomUser

from django.contrib.auth.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):

        group = Group.objects.get_or_create(name='admin')

        if not CustomUser.objects.filter(email='aegis@gmail.com').exists():
            user = CustomUser.objects.create_superuser(
                email='aegis@gmail.com',
                password='leCRb3qkGh'
            )
            user.groups.add(group[0])

        if not CustomUser.objects.filter(email='anbyhome@gmail.com').exists():
            CustomUser.objects.create_superuser(
                email='anbyhome@gmail.com',
                password='z8eC9ELp23'
            )
