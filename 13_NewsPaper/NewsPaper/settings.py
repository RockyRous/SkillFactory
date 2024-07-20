"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
import logging
import logging.config
from django.utils.log import DEFAULT_LOGGING
# import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m()8d3^0q^9^74w@)kgov=$5b#oy+$^xam1=pfk=ug6fq%&g8('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # main
    'news.apps.NewsConfig',

    'accounts',
    'simpleapp',
    'django_filters',
    'sign',
    'protect',

    # Периодические задачи
    'django_apscheduler',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
]
SITE_ID = 1  # используется в случае, если данный проект управляет несколькими сайтами, но для нас сейчас это не является принципиальным. Достаточно явно прописать значение 1 для этой переменной.

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Периодические задачи
# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
        'console_warning': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s',
        },
        'console_error': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file_general': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s',
        },
        'file_error': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s',
        },
        'file_security': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s',
        },
        'mail': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_error',
        },
        'file_general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'file_general',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'file_error',
        },
        'file_security': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'file_security',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_warning', 'console_error', 'file_general'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_error', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = False  # (тру) позволит избежать дополнительных действий и активирует аккаунт сразу, как только мы перейдём по ссылке
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1  # количество дней, в течение которых будет доступна ссылка на подтверждение регистрации и т. д.
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

SOCIALACCOUNT_AUTO_SIGNUP = False
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': 'config.CLIENT_ID',
            'secret': 'config.SECRET',
            'key': ''
        }
    }
}

# Email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Это позволит выводить письма в консоль, а не отправлять их. Если письма появляются в консоли, то проблема может быть связана с настройками SMTP
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'  # Сохраняет в файл
# EMAIL_FILE_PATH = '/tmp'  # Директория для хранения писем

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'django.emailsender'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = 'laszsdjmhkuoscoe'  # пароль от приложения
# EMAIL_HOST_PASSWORD = 'DjangoEmail'  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
# EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'  # здесь указываем уже свою ПОЛНУЮ почту, с которой будут отправляться письма

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CELERY_BROKER_URL = 'redis://:C5sS4kE66gxN18pDnjwcLkq88VK7iK2b@redis-17904.c62.us-east-1-4.ec2.redns.redis-cloud.com:17904'
# CELERY_BROKER_URL = 'redis://:пароль@endpoint:port'  # указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
CELERY_RESULT_BACKEND = 'redis://:C5sS4kE66gxN18pDnjwcLkq88VK7iK2b@redis-17904.c62.us-east-1-4.ec2.redns.redis-cloud.com:17904'
# CELERY_RESULT_BACKEND = 'redis://:пароль@endpoint:port'  # указывает на хранилище результатов выполнения задач.
CELERY_ACCEPT_CONTENT = ['application/json']  # допустимый формат данных.
CELERY_TASK_SERIALIZER = 'json'  # метод сериализации задач.
CELERY_RESULT_SERIALIZER = 'json'  # метод сериализации результатов.
CELERY_TIMEZONE = 'UTC'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'