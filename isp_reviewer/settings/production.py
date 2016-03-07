from base import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

ALLOWED_HOSTS = ['*']

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'isp',
        'USER': 'isp',
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '',
    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }
####

########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'US/Eastern'

CONTACT_EMAIL = 'sth@sth.com'

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

#See: https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#the-set-language-redirect-view
LANGUAGE_COOKIE_NAME = "LANG"

# 30 days
LANGUAGE_COOKIE_AGE = 60*60*24*30

#
LANGUAGES = (
    ('fa', ('Farsi')),
    ('en', ('English')),
)

########## END GENERAL CONFIGURATION

########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
'''
Extremely important, removing any trailing comma after os.path.join() or any other settings, otherwise you may see
an error in admin panel
'''
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'MEDIA')
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
# you can add domain.com to MEDIA_URL as well
MEDIA_URL = ''
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = (
    os.path.join(BASE_DIR, 'static')
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
     #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
########## END STATIC FILE CONFIGURATION


COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


# Logging configuration
"""
    DEBUG: Low level system information for debugging purposes
    INFO: General system information
    WARNING: Information describing a minor problem that has occurred.
    ERROR: Information describing a major problem that has occurred.
    CRITICAL: Information describing a critical problem that has occurred.

    When a message is given to the logger, the log level of the message is compared to the log level of the logger.
    If the log level of the message meets or exceeds the log level of the logger itself,
    the message will undergo further processing. If it doesn't, the message will be ignored.
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    #allow you to restrict the type of messages that are sent from the logger to the handler
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    # the handler is an engine that determines what to do with a message when it is received from the logger
    # level means to log anything DEBUG or higher (which includes all levels) with this handler.
    # You can define other type of  logging by setting it's proper class
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'application_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/isp.log',
            'formatter': 'verbose'
        },
    },
    # Finally, we will declare two loggers to be used, one for the django core and one for our application:
    # a logger is the object that we will use to pass messages to the logging system
    'loggers': {
        'django': {
            'handlers': ['django'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # app name and not the project name
        'accounts': {
            'handlers': ['application_log'],
            'level': 'DEBUG',
        },
    }  # end of logger
}
########## END OF LOGGING


########## EMAIL SETUP

########## END EMAIL SETUP



# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION


########## Admin template

########## END ADMIN TEMPLATE
