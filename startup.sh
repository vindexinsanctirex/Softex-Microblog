#!/usr/bin/env bash

echo "🚀 Iniciando..."

# Migrações
python manage.py migrate --noinput

# Criar admin (SCRIPT)
python create_render_admin.py

# Static files
python manage.py collectstatic --noinput

# Iniciar
exec gunicorn blog_animais_raros.wsgi:application --bind 0.0.0.0:$PORT