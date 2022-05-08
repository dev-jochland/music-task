from django.core.management.base import BaseCommand

from metadata.util import write_csv_to_database


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print(write_csv_to_database('works_metadata.csv'))
        except Exception as e:
            print(e)
