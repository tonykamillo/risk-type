from .base import *

ALLOWED_HOSTS = [
    '.amazonaws.com'
]

DB_BUCKET = 'risktype-db-bucket-dev'

DATABASES = {
    'default': {
        'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
        'NAME': 'db.dev.sqlite3',
        'BUCKET': DB_BUCKET
    }
}
