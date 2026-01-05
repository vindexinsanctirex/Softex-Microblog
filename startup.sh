#!/usr/bin/env bash
# startup.sh - VERSÃO ULTRA SIMPLES PARA RENDER

echo "🚀 INICIANDO BLOG NO RENDER..."

# 1. MIGRAÇÕES
echo "🗄️  Aplicando migrações..."
python manage.py migrate --noinput

# 2. CRIAR ADMIN (FORÇADO)
echo "👑 Criando admin..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
import os

# Deletar admin existente
User.objects.filter(username='admin').delete()

# Criar novo admin
admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
admin_email = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')

User.objects.create_superuser('admin', admin_email, admin_password)
print(f"✅ Admin criado!")
print(f"   👤 Usuário: admin")
print(f"   🔐 Senha: {admin_password}")
EOF

# 3. STATIC FILES
echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# 4. INICIAR
echo "✅ PRONTO! Iniciando servidor..."
exec gunicorn blog_animais_raros.wsgi:application --bind 0.0.0.0:$PORT