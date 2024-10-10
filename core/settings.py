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
    "localhost",
    "www.ksparseh.com",
    "cms.ksparseh.com",
    "www.cms.ksparseh.com",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
   'http://localhost:3001',
   'http://127.0.0.1:3001',
   'https://ksparseh.com',
   'https://www.ksparseh.com',
   'https://cms.ksparseh.com',
   'https://www.cms.ksparseh.com',
   'https://cms.ksparseh.com'
]


# Application definition

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # internal apps 
    'config.apps.ConfigConfig',
    'project.apps.ProjectConfig',
    'blog.apps.BlogConfig',
    'product.apps.ProductConfig',
    'user.apps.UserConfig',
    'template.apps.TemplateConfig',
    'driver.apps.DriverConfig',
    'order.apps.OrderConfig',
    'authentication.apps.AuthenticationConfig',
    # external apps 
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    'nested_inline',
    'django_summernote',
    'rest_framework_simplejwt',
    'jalali_date'
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
]

ROOT_URLCONF = 'core.urls'

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
    ],
    "DEFAULT_THROTTLE_RATES" : {
        "otp" : "1/min"
    }
}


# SIMPLE JWT 

ACCESS_TOKEN_LIFETIME = timedelta(minutes=60)
SLIDING_TOKEN_REFRESH_LIFETIME = timedelta(days=1)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME" : ACCESS_TOKEN_LIFETIME ,
    "SLIDING_TOKEN_REFRESH_LIFETIME" : SLIDING_TOKEN_REFRESH_LIFETIME ,
    "SLIDING_TOKEN_LIFETIME" : timedelta(hours=1),
    "SLIDING_TOKEN_LIFETIME_LATE_USER" : timedelta(hours=2),
    "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER" : timedelta(days=1)
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