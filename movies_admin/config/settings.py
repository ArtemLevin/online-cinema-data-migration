import os
from pathlib import Path
from split_settings.tools import include
from dotenv import load_dotenv

load_dotenv()

include('components/database.py', 'components/installed_apps.py', 'components/middleware.py',
        'components/allowed_hosts.py', 'components/templates.py', 'components/auth_password_validators.py')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

LOCALE_PATHS = ['movies/locale']

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
