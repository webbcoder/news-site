import os
import environ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# env = environ.Env()
# environ.Env.read_env(env_file=os.path.join(str(BASE_DIR), '.env'))
# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DATABASE_ENGINE'),
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': os.getenv('POSTGRES_PORT'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sitedb',
        'USER': 'admin',
        'PASSWORD': '111',
        'HOST': 'db',
        'PORT': '5432',
    }
}
DEBUG = True
