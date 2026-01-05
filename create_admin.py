#!/usr/bin/env python
# create_admin.py - Criar admin localmente
import os
import sys

print("=" * 60)
print("👑 CRIANDO ADMIN LOCALMENTE")
print("=" * 60)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_animais_raros.settings')

try:
    import django
    django.setup()
except Exception as e:
    print(f"❌ Erro ao configurar Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User

# Credenciais
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@animaisraros.com'
ADMIN_PASSWORD = 'admin123'  # Senha SIMPLES para desenvolvimento

print(f"\n🔧 Configurando admin...")
print(f"   👤 Usuário: {ADMIN_USERNAME}")
print(f"   📧 Email: {ADMIN_EMAIL}")
print(f"   🔐 Senha: {ADMIN_PASSWORD}")

try:
    # Deletar admin existente (se houver)
    User.objects.filter(username=ADMIN_USERNAME).delete()
    print("   🗑️  Admin anterior removido")
    
    # Criar novo admin
    admin = User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD
    )
    
    print(f"\n✅ ADMIN CRIADO COM SUCESSO!")
    print(f"📋 Credenciais salvas:")
    print(f"   • Usuário: {ADMIN_USERNAME}")
    print(f"   • Senha: {ADMIN_PASSWORD}")
    print(f"   • Email: {ADMIN_EMAIL}")
    
    print(f"\n🔗 Acesse: http://localhost:8000/admin/")
    print(f"💡 Dica: Execute 'python manage.py runserver' primeiro")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print(f"\n📌 Solução:")
    print(f"1. Execute primeiro: python manage.py migrate")
    print(f"2. Depois execute este script novamente")

print("\n" + "=" * 60)