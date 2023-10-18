
import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+)ka1vlb=6#g!(q_itf^$rrzh(=v=oxt6omd@f&iz=sc26#6e@"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'index'

# Application definition
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.beguirebels.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'contacto@beguirebels.com'
EMAIL_HOST_PASSWORD = '~9Mgyy+D3I6$'

PASSWORD_RESET_TIMEOUT_DAYS = 1  # Cambia esto según tus preferencias
PASSWORD_RESET_EMAIL_SUBJECT = 'Recuperación de contraseña'
PASSWORD_RESET_EMAIL_TEMPLATE_NAME = 'password_reset_email.html'

PANDASCORE_BASE_URL = "https://api.pandascore.co/"
PANDASCORE_HEADERS = {"accept": "application/json", "authorization": "Bearer 6oXS-NlCHvzxRzWsDNQwzIVWgchAGih-5pPAIT4iAJgrT3Wo_kE"}



CRONJOBS=[
    ('*/1 * * * *','EsportHub.cron.enviar_notificaciones','>> /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain/cron_output.log '),
]

# * * * * * /Users/facuhansen/Desktop/EsportsHubWorkSpace/entorno/bin/python /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain/manage.py runcrons >> /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain/log/runcrons.log 2>&1

STATIC_URL = 'static/'


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'EsportHub',
    'django_crontab'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "EsportsHubMain.urls"
SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "EsportHub/templates")],  # Asegúrate de que esta línea esté presente
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "EsportsHubMain.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
