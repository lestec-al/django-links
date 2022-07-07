from pathlib import Path
import os
from boto.s3.connection import S3Connection

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = S3Connection(os.environ['SECRET_KEY'])
except:
    SECRET_KEY = "django-insecure-b$506shp"

# SECURITY WARNING: don't run with debug turned on in production!
if SECRET_KEY == "django-insecure-b$506shp":
    DEBUG = True
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    ALLOWED_HOSTS = ["url-cuter.herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'links',
    'crispy_forms',
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
if DEBUG == False:
    MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'csp.middleware.CSPMiddleware',
    ]

ROOT_URLCONF = 'links_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'links_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    } if DEBUG == True else {
        'ENGINE': S3Connection(os.environ['DATABASE_ENGINE']),
        'NAME': S3Connection(os.environ['DATABASE_NAME']),
        'USER': S3Connection(os.environ['DATABASE_USER']),
        'PASSWORD': S3Connection(os.environ['DATABASE_PASSWORD']),
        'HOST': S3Connection(os.environ['DATABASE_HOST']),
        'PORT': S3Connection(os.environ['DATABASE_PORT']),
        'CONN_MAX_AGE': S3Connection(os.environ['DATABASE_CONN_MAX_AGE']),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
BASE_DIR1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR1, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR1, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Deploying
if DEBUG == False:

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    CSP_DEFAULT_SRC = ("'self'", )

    CSP_STYLE_SRC = ("'self'",
        "'unsafe-inline'",
        'cdn.jsdelivr.net',
        'stackpath.bootstrapcdn.com')

    CSP_SCRIPT_SRC = ("'self'",
        'ajax.cloudflare.com',
        'static.cloudflareinsights.com',
        'www.google-analytics.com',
        'ssl.google-analytics.com',
        'cdn.ampproject.org',
        'www.googletagservices.com',
        'pagead2.googlesyndication.com',
        'stackpath.bootstrapcdn.com',
        'cdn.jsdelivr.net',
        'code.jquery.com')

    CSP_IMG_SRC = ("'self'",)

    CSP_FONT_SRC = ("'self'", )
    CSP_CONNECT_SRC = ("'self'",
        'www.google-analytics.com' )
    CSP_OBJECT_SRC = ("'self'", )
    CSP_BASE_URI = ("'self'", )
    CSP_FRAME_ANCESTORS = ("'self'", )
    CSP_FORM_ACTION = ("'self'", )
    CSP_INCLUDE_NONCE_IN = ('script-src', )
    CSP_MANIFEST_SRC = ("'self'", )
    CSP_WORKER_SRC = ("'self'", )
    CSP_MEDIA_SRC = ("'self'", )