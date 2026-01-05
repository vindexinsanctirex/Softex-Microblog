#!/usr/bin/env python
# fix_admin.py - CORREÇÃO DEFINITIVA DO ADMIN
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_animais_raros.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Erro ao configurar Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User
from blog.models import AnimalRaro
from django.utils import timezone

print("=" * 60)
print("🔧 CORREÇÃO DEFINITIVA DO ADMIN")
print("=" * 60)

# 1. DELETAR ADMIN EXISTENTE (se houver)
print("\n1. 🗑️  Limpando admin existente...")
User.objects.filter(username='admin').delete()
print("   ✅ Admin antigo removido")

# 2. CRIAR NOVO ADMIN COM CREDENCIAIS CORRETAS
print("\n2. 👑 Criando novo superusuário...")

# Credenciais - use variáveis de ambiente ou padrão
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin123!')

print(f"   👤 Usuário: {ADMIN_USERNAME}")
print(f"   📧 Email: {ADMIN_EMAIL}")
print(f"   🔐 Senha: {ADMIN_PASSWORD}")

try:
    # Criar superusuário CORRETAMENTE
    admin = User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD
    )
    
    # Verificar se foi criado corretamente
    admin.refresh_from_db()
    print(f"   ✅ Superusuário criado com sucesso!")
    print(f"   • is_superuser: {admin.is_superuser}")
    print(f"   • is_staff: {admin.is_staff}")
    print(f"   • is_active: {admin.is_active}")
    
except Exception as e:
    print(f"   ❌ Erro ao criar admin: {e}")
    sys.exit(1)

# 3. VERIFICAR SE PODE FAZER LOGIN
print("\n3. 🔐 Testando login...")
try:
    test_user = User.objects.get(username=ADMIN_USERNAME)
    if test_user.check_password(ADMIN_PASSWORD):
        print(f"   ✅ Login testado com SUCESSO!")
        print(f"   • Senha verificada: OK")
    else:
        print(f"   ❌ Senha NÃO corresponde!")
except Exception as e:
    print(f"   ❌ Erro no teste: {e}")

# 4. CRIAR ALGUNS ANIMAIS (se banco vazio)
print("\n4. 🐾 Verificando animais...")
if AnimalRaro.objects.count() == 0:
    print("   ℹ️  Criando animais de exemplo...")
    
    animais = [
        {
            'titulo': 'Mico-leão-dourado',
            'nome_cientifico': 'Leontopithecus rosalia',
            'texto': 'Primata raro da Mata Atlântica brasileira.',
            'categoria': 'MAMIFERO',
            'estado_conservacao': 'EM',
            'regiao_brasil': 'Mata Atlântica - RJ',
            'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Golden_lion_tamarin_portrait3.jpg/800px-Golden_lion_tamarin_portrait3.jpg',
        },
        {
            'titulo': 'Ararajuba',
            'nome_cientifico': 'Guaruba guarouba',
            'texto': 'Ave endêmica da Amazônia brasileira.',
            'categoria': 'AVE',
            'estado_conservacao': 'VU',
            'regiao_brasil': 'Amazônia - PA',
            'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Guaruba_guarouba_-Bird_Park_-Foz_do_Iguacu%2C_Brazil-8a.jpg/800px-Guaruba_guarouba_-Bird_Park_-Foz_do_Iguacu%2C_Brazil-8a.jpg',
        },
    ]
    
    for dados in animais:
        animal = AnimalRaro.objects.create(
            titulo=dados['titulo'],
            nome_cientifico=dados['nome_cientifico'],
            autor=admin,
            texto=dados['texto'],
            categoria=dados['categoria'],
            estado_conservacao=dados['estado_conservacao'],
            regiao_brasil=dados['regiao_brasil'],
            imagem_url=dados['imagem_url'],
        )
        animal.publicar()
        print(f"   ✅ {dados['titulo']}")
    
    print(f"   🎉 {len(animais)} animais criados")
else:
    print(f"   ✅ {AnimalRaro.objects.count()} animais já existem")

# 5. RESUMO FINAL
print("\n" + "=" * 60)
print("🎉 CORREÇÃO CONCLUÍDA!")
print("=" * 60)
print("\n📋 CREDENCIAIS DO ADMIN:")
print(f"   🌐 URL: https://SEU-SITE.onrender.com/admin/")
print(f"   👤 Usuário: {ADMIN_USERNAME}")
print(f"   🔐 Senha: {ADMIN_PASSWORD}")
print(f"   📧 Email: {ADMIN_EMAIL}")
print("\n🔧 PARA TESTAR:")
print("   1. Acesse a URL acima")
print("   2. Use as credenciais")
print("   3. Deve funcionar agora!")
print("\n" + "=" * 60)