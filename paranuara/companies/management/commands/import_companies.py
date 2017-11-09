import json
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from paranuara.companies.models import Company


class Command(BaseCommand):
    help = 'Import all companies from a specified raw json file.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        with open(options['file_path']) as f:
            data = json.load(f)
            for company_data in data:
                try:
                    company = Company(id=company_data['index'],
                                      name=company_data['company'])
                    company.save(force_insert=True)
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(
                        'Company already imported: {}'.format(company))
                    )

        self.stdout.write(self.style.SUCCESS('Import complete.'))
