import os
from os.path import dirname, basename, abspath, expanduser
from sys import path
# Original
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
BASE_DIR = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.debug',
    'django.contrib.auth.context_processors.auth',
)
########## END DEBUG CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
home = expanduser('~')
with open(home + '/.isp_secret_key.txt') as f:
    SECRET_KEY = f.read().strip()
########## END SECRET CONFIGURATION

home = expanduser('~')
with open(home + '/.isp_db_password.txt') as f:
    DB_PASSWORD = f.read().strip()


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## AUTHORIZATION MODEL
AUTH_USER_MODEL = 'accounts.User'
########## END AUTHORIZATION MODEL


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Sites and domain functionality
    # 'django.contrib.sites',

    #admin template
    # 'django_admin_bootstrapped',
    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django-secure lets you run checksecure which checks for security settings for deployment',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'rest_framework',
    'compressor',
    'djangosecure',
    'accounts',
    'NDT',
    'isp',
    'cities_light',
    'locations',
    'contact',
    'admin_ip_whitelist',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_ip_whitelist.middleware.AdminAcceessIPWhiteListMiddleware'
)
########## END MIDDLEWARE CONFIGURATION

########## Whitelisitng the admin
# Remember you have to restart the application everytime you change the ips in the db
ADMIN_ACCEES_WHITELIST_ENABLED = True

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
# which is equal to ROOT_URLCONF = 'no2filter.urls'
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
# equal to WSGI_APPLICATION = 'no2filter.wsgi.application'
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME
########## END WSGI CONFIGURATION



########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#localization-how-to-create-language-files
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )
########## END GENERAL CONFIGURATION

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# All the security related settings
SESSION_COOKIE_PATH = '/;HttpOnly'
# SESSION_COOKIE_SECURE = True
SECURE_FRAME_DENY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS  = 10
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = False

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'generic': '20/minute',
    },
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

