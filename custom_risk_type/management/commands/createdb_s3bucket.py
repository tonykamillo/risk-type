import boto3
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create database bucket'

    def handle(self, *args, **options):

        try:
            s3 = boto3.client('s3')
            s3.create_bucket(Bucket=settings.DB_BUCKET)
            self.stdout.write(self.style.SUCCESS('Successfully created bucket'))
        except Exception as e:
            raise CommandError(str(e))
