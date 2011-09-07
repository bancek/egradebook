#-*- coding: utf-8 -*-

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(1, os.path.join(PROJECT_ROOT, 'lib'))

import pymysql
pymysql.install_as_MySQLdb()

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

ADMINS = (
    (u'Admin', 'email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'eredovalnica',                      # Or path to database file if using sqlite3.
        'USER': 'eredovalnica',                      # Not used with sqlite3.
        'PASSWORD': 'some password',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Ljubljana'

LANGUAGE_CODE = 'sl'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = '=^kmzkzuz#w-x$%vk@d#0vee#xreu067^^6z&_l6vv5^kihblb'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

if DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'authprofile.middleware.UserProfileMiddleware',
    'core.middleware.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
]

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'templates'),
]

INTERNAL_IPS = [] # ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.markup',
    
    'django_extensions',
    'south',
    'compressor',
    'concurrent_server',
    'debug_toolbar',
    'uni_form',
    'autoadmin',
    
    'auth',
    'authprofile',
    'core',
    'dijak',
    'infosys',
    'profesor',
    'stars',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'authprofile.UserProfile'

LOGIN_URL = '/prijava'

LOGOUT_URL = '/odjava'

LOGIN_REDIRECT_URL = '/'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

SENDER_EMAIL = 'email@example.com'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[eRedovalnica] '

COMPRESS = True

try:
    from local_settings import *
except ImportError:
    pass
