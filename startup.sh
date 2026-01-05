#!/usr/bin/env bash
# startup.sh - VERSÃO FINAL TESTADA

echo "🌿 INICIANDO BLOG ANIMAIS RAROS..."

# 1. MIGRAÇÕES (vão para o banco correto)
echo "🗄️  Aplicando migrações..."
python manage.py migrate --noinput
echo "✅ Migrações concluídas"

# 2. DEBUG E CRIAÇÃO DO ADMIN (SÓ NO RENDER)
if [ -n "$RENDER" ]; then
    echo "🌍 AMBIENTE RENDER DETECTADO"
    echo "🔧 Executando diagnóstico e criação do admin..."
    python debug_render.py
else
    echo "💻 Ambiente local - Modo desenvolvimento"
fi

# 3. STATIC FILES
echo "🎨 Processando arquivos estáticos..."
python manage.py collectstatic --noinput
echo "✅ Arquivos estáticos prontos"

# 4. INICIAR
echo "🚀 Iniciando servidor Gunicorn..."
exec gunicorn blog_animais_raros.wsgi:application --bind 0.0.0.0:$PORT