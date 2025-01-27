
import os
import sys
from pathlib import Path
import dj_database_url
from datetime import timedelta
from dotenv import load_dotenv

 # Load environment variables from .env file
load_dotenv()


SIMPLE_JWT = {
    'USER_ID_FIELD': 'employer_id',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
}
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'garnishment_library'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4j-q2^gpu9&%imydt@@vq*h0i#9#(yv0)&q5ewvaftj(eocs2='

# # SECURITY WARNING: don't run with debug turned on in production!
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]


DEBUG = os.environ.get('DEBUG','False')=="False"
STATIC_URL = '/static/'
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['.vercel.app', 'garnishment-backend.vercel.app','http://127.0.0.1:8000/','https://garnishment-backend.render.app']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    # 'celery',
    # 'django-celery-results',
    'User_app',]

AUTHENTICATION_BACKENDS=[
    'django.contrib.auth.backends.ModelBackend'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'User_app.middleware.APICallLoggerMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'auth_project.urls'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://garnishment-backend.onrender.com", 
]


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


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

# Celery Configuration
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'  # Use Redis as broker
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Django-Celery-Results

CELERY_RESULT_BACKEND = 'django-db'



# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }




# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES ={
#     'default' :{
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME' : 'granishmentdb',
#         'HOST' : 'database-1.ctcyyq8ooo4x.eu-north-1.rds.amazonaws.com',
#         'USER' : 'admin',
#         'PASSWORD': 'Orang*#_0107-',
#         'PORT': '3306',
#                 'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'",
#         },
#     }
# }

# import os

# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',

#         'NAME': os.getenv('DB_NAME', 'garnishment-db'),  # Default to 'local_db_name' if DB_NAME is not set
#         'USER': os.getenv('DB_USER', 'garnish-dev@garnish-dev1'),  # Default to 'local_db_user' if DB_USER is not set
#         'PASSWORD': os.getenv('DB_PASSWORD', 'G@rnish-D3v'),  # Default to 'local_db_password'
#         'HOST': os.getenv('DB_HOST', 'garnish-dev1.database.windows.net'),  # Default to 'localhost' if DB_HOST is not set
#         'PORT': os.getenv('DB_PORT', '1433'),  # Default to '1433' if DB_PORT is not set
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'extra_params': 'TrustServerCertificate=yes;',
#         },
#     },
# }


# postgres://gdb_9usu_user:1WIRSGucNXebb5DcoSI1e2hp7RNSuRwn@dpg-cpa5u6dds78s73crqbag-a.singapore-postgres.render.com/gdb_9usu'

BASE_DIR = Path(__file__).resolve().parent.parent




DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}
LANGUAGE_CODE = 'en-us'
USE_I18N = False


FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100 MB

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


WSGI_APPLICATION = 'auth_project.wsgi.app'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'rohan989800@gmail.com'
EMAIL_HOST_PASSWORD = 'vugp wsuc jert ubiu'