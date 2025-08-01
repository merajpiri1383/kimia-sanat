import os 
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*^60c)fy-fd=$@38z4*5t=wnfl_(^1kfn_ja6n^+m7y&a=6qd5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG",False)

ALLOWED_HOSTS = [
    "db.ksparseh.com",
    "www.db.ksparseh.com",
    "cms.ksparseh.com",
    "www.cms.ksparseh.com",
    "ksparseh.com",
    "www.ksparseh.com",
    "localhost",
    "127.0.0.1",
    "91.107.134.107"
]

CSRF_TRUSTED_ORIGINS = [
    "https://db.ksparseh.com",
    "https://www.db.ksparseh.com",
    "https://cms.ksparseh.com",
    "https://www.cms.ksparseh.com",
    "https://ksparseh.com",
    "https://www.ksparseh.com",
    "http://localhost",
    "http://127.0.0.1",
    "https://91.107.134.107"
]


# Application definition

CORS_ALLOW_ALL_ORIGINS = True

STATIC_ROOT = BASE_DIR / "static"

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # internal apps 
    'user.apps.UserConfig',
    'config.apps.ConfigConfig',
    'project.apps.ProjectConfig',
    'blog.apps.BlogConfig',
    'product.apps.ProductConfig',
    'template.apps.TemplateConfig',
    'driver.apps.DriverConfig',
    'order.apps.OrderConfig',
    'authentication.apps.AuthenticationConfig',
    'system.apps.SystemConfig',
    'ticket.apps.TicketConfig',
    'notification.apps.NotificationConfig',
    # external apps 
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    'nested_inline',
    'django_summernote',
    'rest_framework_simplejwt',
    'jalali_date',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'core.urls'

USE_THOUSAND_SEPARATOR = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


AUTH_USER_MODEL = "user.User"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME"),
        'USER' : os.getenv("DATABASE_USER"),
        'PASSWORD' : os.getenv('DATABASE_PASSWORD'),
        'PORT' : os.getenv('DATABASE_PORT',5432),
        'HOST' : os.getenv('DATABASE_HOST'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fa'

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persion')),
    # Add any other languages you want to support
]

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

import locale
locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media"

# celery 
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL","redis://localhost:6379/")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND","redis://localhost:6379/")


# rest framework 
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES" : [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_THROTTLE_RATES" : {
        "otp" : "1/min"
    }
}


# SIMPLE JWT 

ACCESS_TOKEN_LIFETIME = timedelta(days=5)
REFRESH_TOKEN_LIFETIME = timedelta(days=15)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': ACCESS_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME': REFRESH_TOKEN_LIFETIME,
    'ROTATE_REFRESH_TOKENS': True, 
    'BLACKLIST_AFTER_ROTATION': True, 
}

SUMMERNOTE_CONFIG = {
    'attachment_filesize_limit':  int(1024 * 1024 * 1024 // 4 // 3),
    'attachment_absolute_uri': True
}

# jalali date 
JALALI_DATE_DEFAULTS = {
   # if change it to true then all dates of the list_display will convert to the Jalali.
   'LIST_DISPLAY_AUTO_CONVERT': False,
   'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

# theme 

# Configure the color scheme (optional)
ADMIN_INTERFACE_COLOR_SCHEME = {
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
}