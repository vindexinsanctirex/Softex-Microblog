"""
Django settings for blog_animais_raros project.
"""

from pathlib import Path
import os
import sys

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-j()j6yf(g3&8+z!a%(4^+i%b6*m9lw3l*()ma&#e4&11d22&hv')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

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

# ========== DATABASE CONFIG - SIMPLIFICADA E CORRETA ==========

# Verificar se estamos no Render (produção)
if 'RENDER' in os.environ:
    # PRODUÇÃO NO RENDER - PostgreSQL
    print("🚀 Modo: PRODUÇÃO (Render) - Usando PostgreSQL")
    
    # Tentar importar dj_database_url
    try:
        import dj_database_url
        DATABASE_URL = os.environ.get('DATABASE_URL')
        
        if DATABASE_URL:
            DATABASES = {
                'default': dj_database_url.config(
                    default=DATABASE_URL,
                    conn_max_age=600,
                    ssl_require=True
                )
            }
            print(f"✅ PostgreSQL configurado: {DATABASES['default']['HOST']}")
        else:
            print("❌ DATABASE_URL não encontrada no Render!")
            sys.exit(1)
            
    except ImportError:
        print("❌ dj-database-url não instalado. Execute: pip install dj-database-url")
        sys.exit(1)
        
else:
    # DESENVOLVIMENTO LOCAL - SQLite
    print("💻 Modo: DESENVOLVIMENTO LOCAL - Usando SQLite")
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

# ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    '.app.github.dev',
    '.github.dev',
]

# Adicionar host dinâmico do Render se existir
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    print(f"🌐 Host do Render adicionado: {RENDER_EXTERNAL_HOSTNAME}")

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = []

# Adicionar hosts do Render
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.extend([
        f'https://{RENDER_EXTERNAL_HOSTNAME}',
        f'http://{RENDER_EXTERNAL_HOSTNAME}',
    ])

# Adicionar localhost
CSRF_TRUSTED_ORIGINS.extend([
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
])

# Configurações de produção
if 'RENDER' in os.environ:
    DEBUG = False
    print("🔒 Modo PRODUÇÃO - Segurança ativada")
    
    # Configurações de segurança
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # WhiteNoise config (produção)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_MANIFEST_STRICT = False
    
else:
    DEBUG = True
    print("🔓 Modo DESENVOLVIMENTO - Debug ativado")
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Remover print no ambiente de produção
if 'RENDER' not in os.environ:
    print(f"✅ Configuração carregada. DEBUG={DEBUG}")
    print(f"✅ Banco de dados: {DATABASES['default']['ENGINE']}")