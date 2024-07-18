import datetime
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

# BASE DJANGO SETTINGS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['*']
ADMINS = (('Anton Butyrin', 'butyrinhome@gmail.com'), )
DEV_MODE = os.getenv('DEV_MODE')
USE_HIDE = os.getenv('USE_HIDE', False)

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

THIRD_APPS = [
    'channels',
    'corsheaders',
    'drf_spectacular',
    'rest_framework.authtoken',
    'rest_framework',
    'health_check',
    'dj_rest_auth',
    'storages',

    # registration
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',

    # facebook
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
]

CUSTOM_APPS = [
    'applications.core',
    'applications.main',
    'applications.events',
    'applications.sales',
    'applications.users',
    'applications.login',
]

INSTALLED_APPS = ['jazzmin'] + DJANGO_APPS + THIRD_APPS + CUSTOM_APPS + ['django_cleanup']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'applications.main.processors.preference',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'
ASGI_APPLICATION = 'settings.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Mexico/General'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'applications.core.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_nginx')

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

if os.getenv('EMAIL_HOST'):
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    EMAIL_PORT = os.getenv('EMAIL_PORT')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts":[(os.getenv('CHANNEL_HOSTS'), os.getenv('CHANNEL_PORT'))]
        },
    },
}

if os.getenv('GIT_ACTION'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

AUTH_USER_MODEL = 'users.CustomUser'

GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET')
GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = os.path.join(BASE_DIR, "client_secrets.json")
GOOGLE_OAUTH2_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_OAUTH2_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

FACEBOOK_OAUTH2_APP_ID = os.getenv('FACEBOOK_OAUTH2_APP_ID')
FACEBOOK_OAUTH2_APP_SECRET = os.getenv('FACEBOOK_OAUTH2_APP_SECRET')

MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY')
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')

SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=30)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

    'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
]

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'login.serializers.CustomLoginSerializer',
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_ADAPTER = 'applications.login.adapters.CustomAllauthAdapter'

# CORS SETTINGS https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:3000',
]

# JAZZMIN_SETTINGS https://django-jazzmin.readthedocs.io/
JAZZMIN_SETTINGS = {
    "site_title":
    "TicketCrush",
    "site_header":
    "TicketCrush",
    "site_brand":
    "TicketCrush",
    "site_logo":
    'logo.png',
    "login_logo":
    'logo.png',
    "login_logo_dark":
    'logo.png',
    "site_logo_classes":
    "img-circle",
    "site_icon":
    'logo.png',
    "welcome_sign":
    "Welcome to the TicketCrush",
    "copyright":
    "TicketCrush",
    "user_avatar":
    None,
    "topmenu_links": [
        {
            "name": "REDOC",
            "url": "/api/schema/redoc/",
            "new_window": True
        },
        {
            "name": "SWAGGER",
            "url": "/api/schema/redoc/",
            "new_window": True
        },
    ],
    "show_sidebar":
    True,
    "navigation_expanded":
    True,
    "order_with_respect_to": ["auth", "sales", "events", "main"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents":
    "fas fa-chevron-circle-right",
    "default_icon_children":
    "fas fa-circle",
    "related_modal_active":
    True,
    "use_google_fonts_cdn":
    True,
    "show_ui_builder":
    False,
    "changeform_format":
    "collapsible",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "collapsible"
    },
}


# DJANGO REST SETTINGS https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'applications.users.permissions.IsAuthenticatedAndActive',
    # ],
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 200,
    'DEFAULT_FILTER_BACKENDS': [
        # 'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DATE_INPUT_FORMATS': [
        '%d.%m.%Y',
    ],
    'DEFAULT_SCHEMA_CLASS':
    'drf_spectacular.openapi.AutoSchema',

    'AUTH_TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    # 'AUTH_TOKEN_MODEL': 'dj_rest_auth.models.Token'
}

# SPECTACULAR SETTINGS https://drf-spectacular.readthedocs.io/
SPECTACULAR_SETTINGS = {
    'TITLE': 'TicketCrush API',
    'DESCRIPTION': 'Schemas API for TicketCrush',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

try:
    from .local_settings import *  # pylint: disable=wildcard-import
except ImportError:
    pass
