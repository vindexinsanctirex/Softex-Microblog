#!/usr/bin/env python
# debug_simple.py - Debug simplificado
import os
import sys

print("=" * 60)
print("🔍 DEBUG SIMPLIFICADO - BLOG ANIMAIS RAROS")
print("=" * 60)

# 1. Verificar variáveis de ambiente
print("\n1. 🌍 VARIÁVEIS DE AMBIENTE:")
print(f"   • RENDER: {os.environ.get('RENDER', 'NÃO definido')}")
print(f"   • DATABASE_URL: {'DEFINIDA' if os.environ.get('DATABASE_URL') else 'NÃO definida'}")
print(f"   • DEBUG: {os.environ.get('DEBUG', 'NÃO definido')}")

# 2. Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_animais_raros.settings')

try:
    import django
    django.setup()
    print("✅ Django configurado com sucesso")
except Exception as e:
    print(f"❌ Erro ao configurar Django: {e}")
    sys.exit(1)

# 3. Verificar configurações do Django
from django.conf import settings

print(f"\n2. ⚙️  CONFIGURAÇÕES DJANGO:")
print(f"   • DEBUG: {settings.DEBUG}")
print(f"   • DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"   • ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

# 4. Tentar conectar ao banco
print(f"\n3. 🗄️  TESTANDO CONEXÃO COM BANCO...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"   ✅ Conexão com banco OK: {result}")
        
        # Verificar tabelas
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"   📊 {len(tables)} tabelas encontradas")
            if tables:
                print(f"   📋 Primeiras tabelas: {[t[0] for t in tables[:5]]}")
                
except Exception as e:
    print(f"   ❌ Erro na conexão com banco: {e}")

# 5. Verificar usuários (se banco estiver OK)
print(f"\n4. 👥 VERIFICANDO USUÁRIOS...")
try:
    from django.contrib.auth.models import User
    user_count = User.objects.count()
    print(f"   • Total de usuários: {user_count}")
    
    if user_count > 0:
        for user in User.objects.all()[:3]:  # Primeiros 3
            print(f"   • {user.username} - Superuser: {user.is_superuser}")
    
    # Verificar admin específico
    if User.objects.filter(username='admin').exists():
        admin = User.objects.get(username='admin')
        print(f"   ✅ Usuário 'admin' existe")
        print(f"   • Email: {admin.email}")
        print(f"   • Superuser: {admin.is_superuser}")
        print(f"   • Staff: {admin.is_staff}")
    else:
        print(f"   ❌ Usuário 'admin' NÃO existe")
        
except Exception as e:
    print(f"   ❌ Erro ao verificar usuários: {e}")

# 6. Recomendações
print("\n" + "=" * 60)
print("🎯 RECOMENDAÇÕES:")
print("=" * 60)

if 'RENDER' in os.environ:
    print("1. Você está no RENDER (produção)")
    print("2. Use estas credenciais no admin:")
    print(f"   • Usuário: admin")
    print(f"   • Senha: {os.environ.get('ADMIN_PASSWORD', '[verifique variável ADMIN_PASSWORD]')}")
    print(f"3. URL do admin: https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'seu-site')}/admin/")
else:
    print("1. Você está no ambiente LOCAL")
    print("2. Execute primeiro: python manage.py migrate")
    print("3. Depois execute: python create_admin.py")
    print("4. Acesse: http://localhost:8000/admin/")

print("\n" + "=" * 60)