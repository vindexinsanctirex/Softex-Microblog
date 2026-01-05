"""
Django settings for blog_animais_raros project.
"""

from pathlib import Path
import os

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-j()j6yf(g3&8+z!a%(4^+i%b6*m9lw3l*()ma&#e4&11d22&hv')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
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
]

ROOT_URLCONF = 'blog_animais_raros.urls'

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

WSGI_APPLICATION = 'blog_animais_raros.wsgi.application'

# Database
if os.environ.get('DATABASE_URL'):
    # PostgreSQL no Render
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # SQLite local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅✅✅ **DOMÍNIOS CORRETOS DO CODESPACE/GITHUB** ✅✅✅
ALLOWED_HOSTS = [
    # SEU DOMÍNIO ORIGINAL DO CODESPACE/GITHUB:
    '.super-duper-adventure-69vpxgqwj4w4c5rxr-8000.app.github.dev',  # ← SEU DOMÍNIO!
    
    # Para desenvolvimento local:
    'localhost',
    '127.0.0.1',
    
    # Para o Render (se estiver usando):
    '.onrender.com',  # Todos subdomínios do Render
]

# Adicionar host dinâmico do Render se existir
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = []

# ✅ SEU DOMÍNIO DO CODESPACE/GITHUB:
CSRF_TRUSTED_ORIGINS.extend([
    'https://super-duper-adventure-69vpxgqwj4w4c5rxr-8000.app.github.dev',
    'http://super-duper-adventure-69vpxgqwj4w4c5rxr-8000.app.github.dev',
])

# Adicionar host dinâmico do Render (se estiver usando)
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{RENDER_EXTERNAL_HOSTNAME}',
        f'http://{RENDER_EXTERNAL_HOSTNAME}',
    ])

# Adicionar localhost para desenvolvimento
CSRF_TRUSTED_ORIGINS.extend([
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
])

# Configurações de produção
if RENDER_EXTERNAL_HOSTNAME or 'RENDER' in os.environ:
    DEBUG = False
    # Configurações de segurança
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # WhiteNoise config
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_MANIFEST_STRICT = False
else:
    DEBUG = True
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}