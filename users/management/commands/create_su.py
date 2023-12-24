from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='suadmin@sky.pro',
            first_name='Adm',
            last_name='Su',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )

        user.set_password('123qwe456')
        user.save()