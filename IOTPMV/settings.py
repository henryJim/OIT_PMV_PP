"""
Django settings for IOTPMV project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o3vx#lxvn$28bmkd(gv5b%%@m^*zw74_a&msu5#s+ux9!z3_cm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_icons',
    'tasks',
    'usuarios',
    'formacion',
    'gestion_instructores',
    'commons',
    'mptt',
    'matricula',
    'rest_framework',
    'dal',
    'dal_select2',
    'administracion',
    'channels',
    'whitenoise.runserver_nostatic'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'usuarios.middleware.ExpiredSessionMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',  # Nombre único para la caché
    }
}

ROOT_URLCONF = 'IOTPMV.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

SESSION_COOKIE_AGE = 1200

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_SAVE_EVERY_REQUEST = True

ASGI_APPLICATION = 'IOTPMV.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],  # Asegúrate de que Redis esté en ejecución en este host y puerto
        },
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'usuarios.context_processors.perfil',
                'usuarios.context_processors.expiracion_sesion_context'
            ],
        },
    },
]

DJANGO_ICONS = {
    "ICONS": {
        "edit": {"name": "bi bi-pencil"},
        "plus": {"name": "bi bi-plus-lg"},
        "delete": {"name": "bi bi-trash"},
        "detalle": {"name": "bi bi-box-arrow-up-right"},
        "confirmar": {"name": "bi bi-check-square"},
        "asignarapre": {"name": "bi bi-person-fill-up"},
        "archivo": {"name": "bi bi-file-earmark-spreadsheet"},
        "download": {"name": "bi bi-box-arrow-down"},
        "search": {"name": "bi bi-search"},
        "password": {"name": "bi bi-asterisk"},
        "salir": {"name": "bi bi-box-arrow-right"},
        "perfil": {"name": "bi bi-person-bounding-box"},
        "upload": {"name": "bi bi-upload"},
        "x": {"name": "bi bi-x"},
        "confirm": {"name": "bi bi-check2"},
    },
}

WSGI_APPLICATION = 'IOTPMV.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oit_senatic',
        'USER': 'oit_app',
        'PASSWORD': 'N7t5kecjWs55FT1',
        'HOST': '192.168.208.1',
        'PORT': '3306',
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

LANGUAGE_CODE = 'es'

USE_L10N = True

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Carpeta para almacenar archivos subidos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/signin/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Configuración de correo en Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Si usas Gmail o el servidor de correo de tu elección
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'andrelipe897@gmail.com'
EMAIL_HOST_PASSWORD = 'tadg xqga lxsn jxtq'
DEFAULT_FROM_EMAIL = 'andrelipe897@gmail.com'  # El correo desde el cual se enviarán los mensajes

# Formatos de fecha aceptados
DATE_INPUT_FORMATS = ['%d/%m/%Y', '%Y-%m-%d']