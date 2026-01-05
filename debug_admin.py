# debug_admin.py
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_animais_raros.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import AnimalRaro

print("=" * 60)
print("🔍 DEBUG DO BANCO DE DADOS")
print("=" * 60)

# 1. Verificar usuários
print("\n1. 👥 USUÁRIOS NO BANCO:")
users = User.objects.all()
if users:
    for user in users:
        print(f"   • {user.username} ({user.email})")
        print(f"     - Superuser: {user.is_superuser}")
        print(f"     - Staff: {user.is_staff}")
        print(f"     - Ativo: {user.is_active}")
else:
    print("   ❌ NENHUM usuário encontrado!")

# 2. Verificar senha do admin
print("\n2. 🔐 VERIFICANDO SENHA DO ADMIN:")
if User.objects.filter(username='admin').exists():
    admin = User.objects.get(username='admin')
    print(f"   • Admin existe")
    print(f"   • Hash da senha: {admin.password[:50]}...")
    
    # Testar senha
    test_password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
    if admin.check_password(test_password):
        print(f"   ✅ Senha '{test_password}' está CORRETA")
    else:
        print(f"   ❌ Senha '{test_password}' está INCORRETA")
else:
    print("   ❌ Usuário 'admin' NÃO existe")

# 3. Verificar animais
print("\n3. 🐾 ANIMAIS NO BANCO:")
animais_count = AnimalRaro.objects.count()
print(f"   • Total: {animais_count} animais")
if animais_count > 0:
    for animal in AnimalRaro.objects.all()[:3]:  # Primeiros 3
        print(f"   • {animal.titulo} por {animal.autor}")

print("\n" + "=" * 60)
print("🎯 PRÓXIMOS PASSOS:")
print("=" * 60)

# Sugestões baseadas no diagnóstico
if not User.objects.filter(username='admin').exists():
    print("1. ❌ ADMIN NÃO EXISTE")
    print("   Execute: python fix_admin.py")
elif User.objects.filter(username='admin').exists():
    admin = User.objects.get(username='admin')
    if not admin.is_superuser:
        print("2. ❌ ADMIN NÃO É SUPERUSUÁRIO")
        print("   Execute: python fix_admin.py")
    else:
        print("3. ✅ ADMIN EXISTE E É SUPERUSUÁRIO")
        print("   Problema pode ser em:")
        print("   • Static files")
        print("   • Configuração de produção")

print("\nPara corrigir, execute:")
print("python fix_admin.py")