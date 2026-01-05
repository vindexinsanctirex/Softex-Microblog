#!/usr/bin/env bash
# startup.sh - VERSÃO CORRIGIDA PARA STATICFILES

echo "========================================"
echo "🌿 BLOG ANIMAIS RAROS - INICIANDO"
echo "========================================"

# 1. LIMPAR CACHE DE STATICFILES (IMPORTANTE!)
echo "1. 🧹 Limpando cache de staticfiles..."
rm -f staticfiles/.whitenoise.json 2>/dev/null || true

# 2. MIGRAÇÕES DO BANCO
echo "2. 🗄️  Aplicando migrações..."
python manage.py migrate --noinput
echo "   ✅ Migrações aplicadas"

# 3. CRIAR/ATUALIZAR SUPERUSUÁRIO
echo "3. 👑 Verificando superusuário..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
import os

username = 'admin'
email = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')
password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')

try:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'is_staff': True, 'is_superuser': True}
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Superusuário '{username}' CRIADO")
    else:
        # Apenas atualizar senha se necessário
        if not user.check_password(password):
            user.set_password(password)
            user.save()
            print(f"✅ Superusuário '{username}' ATUALIZADO")
        else:
            print(f"✅ Superusuário '{username}' JÁ EXISTE")
    
    print(f"   📧 Email: {email}")
    print(f"   🔐 Senha: [configurada nas variáveis]")
    
except Exception as e:
    print(f"❌ Erro: {e}")
EOF

# 4. COLETAR ARQUIVOS ESTÁTICOS (CORRIGIDO)
echo "4. 🎨 Coletando arquivos estáticos..."
# Limpar pasta staticfiles primeiro
rm -rf staticfiles 2>/dev/null || true
mkdir -p staticfiles

# Coletar estáticos SEM manifest
python manage.py collectstatic --noinput --clear
echo "   ✅ Arquivos estáticos coletados"

# 5. VERIFICAR SE ARQUIVOS DO ADMIN EXISTEM
echo "5. 🔍 Verificando arquivos do Admin..."
if [ -f "staticfiles/admin/css/base.css" ]; then
    echo "   ✅ Arquivos do Admin encontrados"
else
    echo "   ⚠️  Arquivos do Admin não encontrados"
    echo "   🔄 Recriando staticfiles..."
    python manage.py collectstatic --noinput --clear --ignore admin
    # Tentar instalar admin files manualmente
    python -c "import os; from django.conf import settings; print('Admin path:', os.path.join(settings.STATIC_ROOT, 'admin'))"
fi

# 6. RESUMO
echo ""
echo "========================================"
echo "🎉 CONFIGURAÇÃO CONCLUÍDA!"
echo "========================================"
echo "📊 STATUS:"
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from blog.models import AnimalRaro
import os

print(f"   👥 Usuários: {User.objects.count()}")
print(f"   🐾 Animais: {AnimalRaro.objects.count()}")

# Verificar admin files
import django
from django.contrib.admin import apps
admin_path = os.path.join(django.__path__[0], 'contrib', 'admin', 'static', 'admin')
print(f"   📁 Admin static path: {admin_path}")
EOF

echo ""
echo "🔗 ACESSO:"
echo "   🌐 Site: https://softex-microblog.onrender.com"
echo "   ⚙️  Admin: https://softex-microblog.onrender.com/admin/"
echo ""
echo "========================================"

# 7. INICIAR SERVIDOR
exec gunicorn blog_animais_raros.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -