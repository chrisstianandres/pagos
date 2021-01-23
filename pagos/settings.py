"""
Django settings for pagos project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wnhrsff=tzfbm)ci1=43cjf+59i755(*y1a#u48%*zwg(ml^0z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.apps.AppsConfig',

    #core apps
    'apps.categoria',
    'apps.cliente',
    'apps.DatabaseBackups',
    'apps.empresa',
    'apps.gasto',
    'apps.presentacion',
    'apps.producto',
    'apps.proveedor',
    'apps.tipogasto',
    'apps.delvoluciones_venta',
    'apps.user',
    'apps.maquina',
    'apps.reparacion',
    'apps.transaccion',
    'apps.venta',
    'apps.compra',
    'apps.inventario_productos',
    'apps.inventario_material',
    'apps.confeccion',
    'apps.alquiler',
    'apps.material',
    'apps.asignar_recursos',
    'apps.producto_base',
    'apps.sitioweb',
    'apps.produccion',
    'apps.talla',
    'apps.tipo_material',
    'apps.color'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pagos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'pagos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bd_pagos',
        'USER': 'user_bd',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'STORAGE_ENGINE': 'MyISAM / INNODB / ETC'
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-ec'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
    # os.path.join(BASE_DIR, "static"),
    # BASE_DIR / "static",
]
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
#
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")
AUTH_USER_MODEL = 'user.User'


# STATIC_URL = '/static/'
# STATIC_ROOT = 'staticfiles'
#
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')