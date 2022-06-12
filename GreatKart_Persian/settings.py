"""
Django settings for GreatKart_Persian project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7h7!6k7orwf-irp_#-4#!y59rujz^8upv=v7jcg6s6v+1evigr'

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
    # Our applications
    'eshop_Home.apps.EshopHomeConfig',
    'eshop_Accounts.apps.EshopAccountsConfig',
    'eshop_Store.apps.EshopStoreConfig',
    'eshop_Cart.apps.EshopCartConfig',
    'eshop_Orders.apps.EshopOrdersConfig',
    #Bank gateway
    'azbankgateways',
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

ROOT_URLCONF = 'GreatKart_Persian.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'eshop_Home.context_processor.menu_links',
                'eshop_Cart.context_processor.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'GreatKart_Persian.wsgi.application'
AUTH_USER_MODEL = 'eshop_Accounts.Account'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fa-pe'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,"static")]


MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR,'uploads')


from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

#SMTP CONFIGURATION.....

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bahman.gs2020@gmail.com'
EMAIL_HOST_PASSWORD = 'saeed086087'
EMAIL_USE_TLS = True

AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       # 'BMI': {
       #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       #     'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
       #     'SECRET_KEY': '<YOUR SECRET CODE>',
       # },
       # 'SEP': {
       #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       #     'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
       # },
       'ZARINPAL': {
           'MERCHANT_CODE': 'fc5b3f9b-7089-4cc5-a03c-fd90ac73c249',
       },
       # 'IDPAY': {
       #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       #     'METHOD': 'POST',  # GET or POST
       #     'X_SANDBOX': 1,  # 0 disable, 1 active
       # },
       # 'ZIBAL': {
       #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       # },
       # 'BAHAMTA': {
       #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
       # },
       # 'MELLAT': {
       #     'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
       #     'USERNAME': '<YOUR USERNAME>',
       #     'PASSWORD': '<YOUR PASSWORD>',
       # },
   },
   'IS_SAMPLE_FORM_ENABLE': True, # اختیاری و پیش فرض غیر فعال است
   'DEFAULT': 'ZARINPAL',
   'CURRENCY': 'IRR', # اختیاری
   'TRACKING_CODE_QUERY_PARAM': 'tc', # اختیاری
   'TRACKING_CODE_LENGTH': 16, # اختیاری
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader', # اختیاری
   'BANK_PRIORITIES': [
       # 'ZARINPAL'
       # 'SEP',
       # and so on ...
   ], # اختیاری
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'