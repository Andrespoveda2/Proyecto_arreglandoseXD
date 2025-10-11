import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-tdw0#@5fi-22be1=e&flix6-%ry*g2ofnfw8)c6+x$y9g7mb#)'
DEBUG = True
ALLOWED_HOSTS = []

# =========================================================================
# 1. APPLICATION DEFINITION (INSTALLED_APPS)
# Debemos registrar todas nuestras apps y el nuevo Usuario
# =========================================================================

INSTALLED_APPS = [
    # Apps nativas de Django (van primero)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nuestras aplicaciones personalizadas
    'home',
    'usuario',
    'empresas',
    'aprendices',
    'instructores',
    'gestion', 
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

ROOT_URLCONF = 'Prototipo_OASIS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Prototipo_OASIS.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation... (dejamos la validación por defecto)
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

# =========================================================================
# 2. CONFIGURACIÓN DE AUTENTICACIÓN PERSONALIZADA
# Esto es CRUCIAL para que Django use nuestro modelo Usuario
# =========================================================================

AUTH_USER_MODEL = 'usuario.Usuario' 
# En tu urls.py principal, la app 'usuario' está bajo el prefijo 'auth/'.
# La URL de login dentro de esa app se llama 'login'.
# El nombre completo que Django debe resolver es 'auth:login'.
LOGIN_URL = 'auth:login' # Redirección por defecto si no está logueado
LOGIN_REDIRECT_URL = '/auth/redirect/' # La vista que maneja la redirección por rol

# Internationalization... (dejamos los defaults)
LANGUAGE_CODE = 'es-co' # Cambiado a español de Colombia para coherencia
TIME_ZONE = 'America/Bogota' # Zona horaria de Colombia
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Directorio donde `collectstatic` reunirá todos los archivos estáticos para producción.
# Es necesario definirlo para que la función `static()` en urls.py funcione correctamente.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 3. DIRECTORIO ESTÁTICO (Para cargar los CSS, JS, imágenes)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
