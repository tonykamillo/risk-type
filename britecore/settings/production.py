from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    '.amazonaws.com'
]

INSTALLED_APPS = INSTALLED_APPS + [
    'zappa_django_utils',
]

DB_BUCKET = 'risktype-db-bucket'

DATABASES = {
    'default': {
        'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
        'NAME': 'db.sqlite3',
        'BUCKET': DB_BUCKET
    }
}
