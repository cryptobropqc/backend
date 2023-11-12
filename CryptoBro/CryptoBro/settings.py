import os
from datetime import timedelta
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
#SECRET_KEY = 'o-r2-(t(y-evahg09wiya13+zyh(f$*avy_of$z=2m!+j)ae3j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(" ")

#ALLOWED_HOSTS = [
#    'localhost',
#    '127.0.0.1',
#    '[::1]',    
#    '52.91.232.233',
#    'api.cryptobro.pro',
#]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ALLOWED_HOSTS = [
#     'localhost',
#     '127.0.0.1',
#     '[::1]',
#     'testserver',
# ]




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # Для  Api login new
    'rest_framework.authtoken',
    # 'rest_framework_simplejwt',
    'users.apps.UsersConfig',
    'posts.apps.PostsConfig',
    'core.apps.CoreConfig',
    'about.apps.AboutConfig',
    'sorl.thumbnail',
    'api_cryptobro',
    'import_export',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CryptoBro.urls'

# Путь к директории с шаблонами вынесен в переменную:
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Добавлено: Искать шаблоны на уровне проекта
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # Вот оно, нужное:
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Добавлен контекст-процессор
                'core.context_processors.year.year',
            ],
        },
    },
]

CORS_ALLOWED_ORIGINS = [
    "https://test.cryptobro.pro",
    "https://api.cryptobro.pro",
    "https://cryptobro.pro",
]

# Отправка сообщения на почту
DOMAIN_NAME = 'cryptobro.pro'
EMAIL_HOST = f'info@{DOMAIN_NAME}'
DEFAULT_FROM_EMAIL = "info@cryptobro.pro"


WSGI_APPLICATION = 'CryptoBro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#   }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB", ""),
        "USER": os.getenv("POSTGRES_USER", ""),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

# DATABASES = {
#      "default": {
#          "ENGINE": "django.db.backends.postgresql_psycopg2",
#          "NAME": "cryptobro_dev",
#          "USER": "postgres",
#          "PASSWORD": "ldslfnH0-%ka792JKS",
#          "HOST": "cryprobro-db-dev.cmthskjql8iw.us-east-1.rds.amazonaws.com",
#          "PORT": "5432",
#     }
#  }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'posts:index'
# LOGOUT_REDIRECT_URL = 'posts:index'

#  подключаем движок filebased.EmailBackend
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# указываем директорию, в которую будут складываться файлы писем
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

PASSWORD_RESET_URL = 'users:password_reset_form'
PASSWORD_RESET_REDIRECT_URL = 'users:password_reset_done'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

#  Число страниц
COUNT_PAGES = 10

# Абстракция Usera для app reviews
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=20),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


LENG_LOGIN_USER = 150
