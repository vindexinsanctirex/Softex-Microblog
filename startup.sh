#!/usr/bin/env bash
# startup.sh - VERSÃO FINAL CORRETA (não apaga dados)

echo "========================================"
echo "🌿 BLOG ANIMAIS RAROS - INICIANDO"
echo "========================================"

# 1. MIGRAÇÕES DO BANCO
echo "1. 🗄️  Aplicando migrações..."
python manage.py migrate --noinput
echo "   ✅ Migrações aplicadas"

# 2. VERIFICAR/CRIAR SUPERUSUÁRIO (SEM APAGAR!)
echo "2. 👑 Verificando superusuário..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
import os

username = 'admin'
email = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')
password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')

try:
    # Verificar se usuário existe
    user = User.objects.filter(username=username).first()
    
    if user:
        # Usuário EXISTE - apenas atualizar senha se mudou
        if not user.check_password(password):
            user.set_password(password)
            user.save()
            print(f"✅ Superusuário '{username}' EXISTE - senha atualizada")
        else:
            print(f"✅ Superusuário '{username}' EXISTE - pronto para uso")
    else:
        # Usuário NÃO EXISTE - criar novo
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuário '{username}' CRIADO (não existia)")
    
    print(f"\n📋 CREDENCIAIS ATUAIS:")
    print(f"   👤 Usuário: {username}")
    print(f"   📧 Email: {email}")
    print(f"   🔐 Senha: [configurada nas variáveis de ambiente]")
    
except Exception as e:
    print(f"❌ Erro ao verificar/criar superusuário: {e}")
EOF

# 3. VERIFICAR/CRIAR ANIMAIS APENAS SE NECESSÁRIO
echo "3. 🐾 Verificando animais..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from blog.models import AnimalRaro

try:
    # Verificar quantos animais existem
    total_animais = AnimalRaro.objects.count()
    
    if total_animais == 0:
        print("   ⚠️  Nenhum animal encontrado. Criando exemplos...")
        
        user = User.objects.get(username='admin')
        
        animais_base = [
            {
                'titulo': 'Mico-leão-dourado',
                'nome_cientifico': 'Leontopithecus rosalia',
                'texto': 'O mico-leão-dourado é um primata endêmico da Mata Atlântica brasileira.',
                'categoria': 'MAMIFERO',
                'estado_conservacao': 'EM',
                'regiao_brasil': 'Mata Atlântica - RJ',
                'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Golden_lion_tamarin_portrait3.jpg/800px-Golden_lion_tamarin_portrait3.jpg',
            },
            {
                'titulo': 'Ararajuba',
                'nome_cientifico': 'Guaruba guarouba',
                'texto': 'Também conhecida como guaruba, esta ave é endêmica da Amazônia brasileira.',
                'categoria': 'AVE',
                'estado_conservacao': 'VU',
                'regiao_brasil': 'Amazônia - PA',
                'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Guaruba_guarouba_-Bird_Park_-Foz_do_Iguacu%2C_Brazil-8a.jpg/800px-Guaruba_guarouba_-Bird_Park_-Foz_do_Iguacu%2C_Brazil-8a.jpg',
            },
        ]
        
        for dados in animais_base:
            # Criar apenas se não existir
            if not AnimalRaro.objects.filter(titulo=dados['titulo']).exists():
                animal = AnimalRaro.objects.create(
                    titulo=dados['titulo'],
                    nome_cientifico=dados['nome_cientifico'],
                    autor=user,
                    texto=dados['texto'],
                    categoria=dados['categoria'],
                    estado_conservacao=dados['estado_conservacao'],
                    regiao_brasil=dados['regiao_brasil'],
                    imagem_url=dados['imagem_url'],
                )
                animal.publicar()
                print(f"   ✅ {dados['titulo']}")
            else:
                print(f"   ℹ️ {dados['titulo']} (já existe)")
        
        print(f"\n   🎉 {AnimalRaro.objects.count()} animais criados")
    else:
        print(f"   ✅ {total_animais} animais já existem no banco")
        print("   ℹ️  Nenhum animal novo será criado (para não duplicar)")
        
except Exception as e:
    print(f"   ❌ Erro: {e}")
EOF

# 4. COLETAR ARQUIVOS ESTÁTICOS
echo "4. 🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
echo "   ✅ Arquivos estáticos prontos"

# 5. RESUMO FINAL
echo ""
echo "========================================"
echo "🎉 CONFIGURAÇÃO CONCLUÍDA!"
echo "========================================"
echo "📊 RESUMO:"
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from blog.models import AnimalRaro

users = User.objects.count()
animais = AnimalRaro.objects.count()
animais_publicados = AnimalRaro.objects.filter(publicado_em__isnull=False).count()

print(f"   👥 Usuários: {users}")
print(f"   🐾 Animais totais: {animais}")
print(f"   📢 Animais publicados: {animais_publicados}")
EOF

echo ""
echo "🔗 ACESSO:"
echo "   🌐 Site: https://softex-microblog.onrender.com"
echo "   ⚙️  Admin: https://softex-microblog.onrender.com/admin/"
echo ""
echo "========================================"

# 6. INICIAR SERVIDOR
exec gunicorn blog_animais_raros.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -