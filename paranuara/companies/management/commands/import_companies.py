import json
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from companies.models import Company


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
                    company.save()
                    Company(id=company_data['index'],
                                      name=company_data['company']).save()
                except IntegrityError:
                    print('Boob')
                    self.stdout.write(self.style.ERROR(
                        'Company already imported: {}'.format(company))
                    )

        self.stdout.write(self.style.SUCCESS('Import complete.'))
