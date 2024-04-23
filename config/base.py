import os
from pathlib import Path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
import jinja2 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(f"BASE_DIR: {BASE_DIR}")
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Where Django looks for static files
STATIC_ROOT = BASE_DIR / 'collected_static'  # Where static files are collected to

# Media files (User-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' #
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
# Templates
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')  
TEMPLATES_DIR_FULL = os.path.join(BASE_DIR, 'templates/panel/jinja')
ADMIN_TEMPLATE_DIR = os.path.join(BASE_DIR, '/apps/panel/admin/tpl') #c:\Users\User\Desktop\Nest\DEV\apps\panel\admin\tpl
#apps\panel\admin\tpl

#ALLOWED_TAGS#
#win path c:\Users\User\Desktop\Nest\DEV\templates\panel\jinja\jinja_page_manager.html


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [TEMPLATES_DIR, TEMPLATES_DIR_FULL, ADMIN_TEMPLATE_DIR],  # Make sure this is the correct path to your templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'apps.panel.jinja.jinja_renderer.jinja_renderer',
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                #'jinja2.ext.autoescape',
                #'jinja2.ext.with_',
                'django_jinja.builtins.extensions.StaticFilesExtension', # Add this line
                # ... other Jinja2 extensions ...
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # Uncomment or add custom context processors as needed
                # 'apps.panel.templatetags.context_processors.get_site_data',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [str(BASE_DIR / 'templates'), str(ADMIN_TEMPLATE_DIR)],
        'APP_DIRS': True,  # This must be True for Django admin to find its templates
        'OPTIONS': {
            'context_processors': [
                #    django.contrib.admin.templates.admin
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Uncomment or add custom context processors as needed
                # 'apps.panel.templatetags.context_processors.get_site_data',
            ],
        },
    },
]

# Application definition
INSTALLED_APPS = [
    'grappelli',
    #'filebrowser',
    #'django.contrib.sites', # explain: https://docs.djangoproject.com/en/3.2/ref/contrib/sites/
    'django.contrib.humanize', # explain: https://docs.djangoproject.com/en/3.2/ref/contrib/humanize/
    'django.contrib.sitemaps', # 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.panel',
    'mptt',
    'tinymce',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'panel',
        'USER': 'admin',
        'PASSWORD': 'verystronglysecret',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET default_storage_engine=InnoDB; SET collation_connection=utf8mb4_unicode_ci;"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Security
SECRET_KEY = 'django-insecure-c@5c#35)wz380g)$l+$nqmwq5ibdv8+9b7m+k3l^(=mums8dpg'
DEBUG = True
ALLOWED_HOSTS =['*']

# TinyMCE configuration
TINYMCE_DEFAULT_CONFIG = {
    'width': '100%',
    'theme': 'silver',
    'height': '450',
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'powerpaste casechange searchreplace autolink directionality visualblocks visualchars image link media mediaembed codesample table charmap pagebreak nonbreaking anchor tableofcontents insertdatetime advlist lists checklist wordcount tinymcespellchecker editimage help formatpainter permanentpen charmap linkchecker emoticons advtable export autosave advcode fullscreen code', # 'code' plugin added here
    'toolbar': "undo redo print spellcheckdialog formatpainter | blocks fontfamily fontsize | bold italic underline forecolor backcolor | link image | alignleft aligncenter alignright alignjustify | code", # Ensure 'code' button is in the toolbar
}

INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG', # Set the logging level here (e.g. 'INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL')
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'CRITICAL', #
            'propagate': True,
        },
        # ... Define more loggers if needed ...
    },
}

# Debug Toolbar configuration
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# These settings are defined at the beginning of the file

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Additional settings can be defined here

# Make sure to replace 'admin', 'password', 'django-insecure-c@5c#35)wz380g)$l+$nqmwq5ibdv8+9b7m+k3l^(=mums8dpg'
# and other sensitive information with environment variables or other secure storage mechanisms
# before deploying to production.
