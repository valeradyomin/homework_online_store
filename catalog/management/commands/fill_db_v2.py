from django.core.management import BaseCommand, call_command
from django.db import ProgrammingError, IntegrityError
from catalog.models import Category


class Command(BaseCommand):
    requires_migrations_check = True

    def handle(self, *args, **options):

        db_json = 'catalog_data.json'

        Category.objects.all().delete()
        Category.truncate_table_restart_id()

        try:
            call_command('loaddata', db_json)
        except ProgrammingError:
            pass
        except IntegrityError as e:
            self.stdout.write(f'Ошибка: {e}', self.style.NOTICE)
        else:
            self.stdout.write('Команда выполнена успешно', self.style.SUCCESS)