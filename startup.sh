#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando Blog Animais Raros..."

# 1. Migrações
python manage.py migrate --noinput

# 2. Setup dados iniciais (ignora warnings de static)
python manage.py setup_production --skip-static

# 3. Coletar static files apenas se STATIC_ROOT existir
if [ -n "${STATIC_ROOT:-}" ]; then
    python manage.py collectstatic --noinput --clear
fi

# 4. Iniciar servidor
echo "✅ Setup completo! Iniciando servidor..."
exec gunicorn blog_animais_raros.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando Blog Animais Raros..."

# 1. Migrações
python manage.py migrate --noinput

# 2. Setup dados iniciais (ignora warnings de static)
python manage.py setup_production --skip-static

# 3. Coletar static files apenas se STATIC_ROOT existir
if [ -n "${STATIC_ROOT:-}" ]; then
    python manage.py collectstatic --noinput --clear
fi

# 4. Iniciar servidor
echo "✅ Setup completo! Iniciando servidor..."
exec gunicorn blog_animais_raros.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120