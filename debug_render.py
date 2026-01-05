#!/usr/bin/env python
# debug_render.py - Debug ESPECÍFICO para o Render
import os
import sys

print("="*70)
print("🐛 DEBUG ESPECÍFICO PARA O RENDER")
print("="*70)

# 1. Verificar se está no Render
print("1. 🌍 VERIFICANDO AMBIENTE:")
print(f"   • RENDER: {'✅ SIM' if os.environ.get('RENDER') else '❌ NÃO'}")
print(f"   • DATABASE_URL: {'✅ DEFINIDA' if os.environ.get('DATABASE_URL') else '❌ NÃO'}")
print(f"   • ADMIN_PASSWORD: {'✅ ' + os.environ.get('ADMIN_PASSWORD') if os.environ.get('ADMIN_PASSWORD') else '❌ NÃO DEFINIDA'}")

# Sair se não for Render
if not os.environ.get('RENDER'):
    print("\n⚠️  Este ambiente NÃO é o Render. Saindo.")
    sys.exit(0)

# 2. Configurar Django no Render
print("\n2. ⚙️  CONFIGURANDO DJANGO NO RENDER...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_animais_raros.settings')

try:
    import django
    django.setup()
    print("   ✅ Django configurado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    sys.exit(1)

# 3. Verificar banco de dados REAL
from django.conf import settings
from django.db import connection

print(f"\n3. 🗄️  BANCO DE DADOS CONECTADO:")
print(f"   • ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"   • NAME: {connection.settings_dict.get('NAME', 'N/A')}")
print(f"   • HOST: {connection.settings_dict.get('HOST', 'N/A')}")

# 4. Testar conexão e ver usuários
from django.contrib.auth.models import User

print(f"\n4. 👥 USUÁRIOS NO POSTGRESQL DO RENDER:")
try:
    user_count = User.objects.count()
    print(f"   • Total: {user_count} usuários")
    
    if user_count > 0:
        for user in User.objects.all():
            print(f"   • {user.username} - Superuser: {user.is_superuser} - Email: {user.email}")
    else:
        print("   ❌ BANCO VAZIO! Nenhum usuário encontrado.")
        
    # Verificar admin específico
    if User.objects.filter(username='admin').exists():
        admin = User.objects.get(username='admin')
        print(f"\n   ✅ Admin existe no PostgreSQL")
        print(f"   • Email: {admin.email}")
        print(f"   • Superuser: {admin.is_superuser}")
        print(f"   • Hash da senha: {admin.password[:30]}...")
        
        # Testar senha
        test_pass = os.environ.get('ADMIN_PASSWORD', '')
        if test_pass and admin.check_password(test_pass):
            print(f"   🔐 Senha da variável ADMIN_PASSWORD: ✅ CORRETA")
        else:
            print(f"   🔐 Senha da variável ADMIN_PASSWORD: ❌ INCORRETA")
    else:
        print(f"\n   ❌ Admin NÃO existe no PostgreSQL do Render!")
        
except Exception as e:
    print(f"   ❌ Erro ao consultar usuários: {e}")

# 5. Criar admin se não existir
print(f"\n5. 🔧 AÇÃO: CRIANDO ADMIN SE NECESSÁRIO...")
try:
    if not User.objects.filter(username='admin').exists():
        ADMIN_PASS = os.environ.get('ADMIN_PASSWORD', 'SenhaPadrao123!')
        ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')
        
        User.objects.create_superuser('admin', ADMIN_EMAIL, ADMIN_PASS)
        print(f"   ✅ ADMIN CRIADO NO POSTGRESQL!")
        print(f"   • Usuário: admin")
        print(f"   • Senha: {ADMIN_PASS}")
        print(f"   • Email: {ADMIN_EMAIL}")
    else:
        print("   ℹ️  Admin já existe, nenhuma ação necessária")
        
except Exception as e:
    print(f"   ❌ Erro ao criar admin: {e}")

print("\n" + "="*70)
print("🎯 PRÓXIMOS PASSOS:")
print("="*70)
print("1. Adicione este script ao startup.sh do Render")
print("2. Faça deploy e verifique os logs")
print("3. Acesse: https://softex-microblog.onrender.com/admin/")
print("\n" + "="*70)