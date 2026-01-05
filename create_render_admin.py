#!/usr/bin/env python
# create_render_admin.py - Criar admin no Render
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_animais_raros.settings')
django.setup()

from django.contrib.auth.models import User

print("=" * 50)
print("👑 CRIANDO ADMIN PARA O RENDER")
print("=" * 50)

# Credenciais (use variáveis de ambiente no Render)
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'RenderAdmin123!')  # Senha FORTE

print(f"Configurando: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")

try:
    # Remover admin existente
    User.objects.filter(username=ADMIN_USERNAME).delete()
    
    # Criar novo
    admin = User.objects.create_superuser(
        ADMIN_USERNAME,
        ADMIN_EMAIL,
        ADMIN_PASSWORD
    )
    
    print(f"\n✅ ADMIN CRIADO COM SUCESSO!")
    print(f"   👤 Usuário: {ADMIN_USERNAME}")
    print(f"   📧 Email: {ADMIN_EMAIL}")
    print(f"   🔐 Senha: {ADMIN_PASSWORD}")
    print(f"\n🎯 Agora acesse: https://SEU-SITE.onrender.com/admin/")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")

print("\n" + "=" * 50)