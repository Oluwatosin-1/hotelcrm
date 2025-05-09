"""
Django settings for hotelcrm project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-j3t*7nf&8hmv@jivrwpae)q@bi^s-&bw8w44o+(34yf*yaa@_h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", "portal.asfedloungeandsuites.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "billing",
    "expenses",
    "customers",
    "hotel",
    "housekeeping",
    "reports",
    "reservations",
    "restaurant",
    "rooms",
    "crispy_forms",
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.middleware.LoginRequiredMiddleware",  # Add it near the top
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hotelcrm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "accounts.context_processors.clock_status",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hotelcrm.wsgi.application"

AUTH_USER_MODEL = "accounts.User"
# settings.py
LOGIN_REDIRECT_URL = "accounts:dashboard"  # After login, go to dashboard
LOGOUT_REDIRECT_URL = "accounts:signin"  # After logout, go to signin page
LOGIN_URL = "accounts:signin"  # Redirect here if login is required

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # or whichever you’re using
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# # Set session to expire in 30 minutes (1800 seconds)
# SESSION_COOKIE_AGE = 1800  # 30 minutes
# # Ensure session expires when the browser is closed
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# # Enable database-backed session storage (Ensure you run migrations)
# SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# STATIC_URL = "/static/"
# STATIC_ROOT = "/home/skillsqu/hotelcrm/static"
# STATIC_ROOT = '/home/skillsqu/hotelcrm/staticfiles'

# STATICFILES_DIRS = [BASE_DIR / 'static']

# MEDIA_URL = "/media/"
# MEDIA_ROOT = "/home/skillsqu/hotelcrm/media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

# settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yourprovider.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "your_account"
EMAIL_HOST_PASSWORD = "your_password"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "yourhotel@example.com"
