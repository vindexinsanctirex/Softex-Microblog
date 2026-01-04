import os
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import AnimalRaro
from django.utils import timezone

class Command(BaseCommand):
    help = 'Configura dados iniciais para produção'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-static',
            action='store_true',
            help='Pular verificação de arquivos estáticos',
        )
    
    def handle(self, *args, **options):
        skip_static = options['skip_static']
        
        self.stdout.write('=' * 60)
        self.stdout.write('🚀 CONFIGURANDO BLOG ANIMAIS RAROS - SIMPLIFICADO')
        self.stdout.write('=' * 60)
        
        if not skip_static:
            # Apenas verificar/criar pasta static
            static_dir = os.path.join(os.getcwd(), 'static')
            if not os.path.exists(static_dir):
                os.makedirs(static_dir, exist_ok=True)
                self.stdout.write(self.style.SUCCESS('✅ Pasta /static criada'))
        
        # 1. SUPERUSUÁRIO
        self.stdout.write('\n1. 🔐 Configurando superusuário...')
        try:
            if not User.objects.filter(username='admin').exists():
                admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
                admin_email = os.environ.get('ADMIN_EMAIL', 'admin@animaisraros.com')
                
                User.objects.create_superuser(
                    username='admin',
                    email=admin_email,
                    password=admin_password
                )
                self.stdout.write(self.style.SUCCESS('   ✅ Superusuário criado!'))
                self.stdout.write(f'   👤 Usuário: admin')
                self.stdout.write(f'   📧 Email: {admin_email}')
                self.stdout.write(f'   🔐 Senha: {admin_password}')
            else:
                self.stdout.write('   ℹ️ Superusuário já existe')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Erro: {e}'))
            if 'UNIQUE constraint' in str(e):
                self.stdout.write('   ℹ️ Usuário já existe, continuando...')
        
        # 2. ANIMAIS
        self.stdout.write('\n2. 🐾 Criando animais raros...')
        
        animais = [
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
            {
                'titulo': 'Tucano-de-bico-preto',
                'nome_cientifico': 'Ramphastos vitellinus ariel',
                'texto': 'Tucano raro da Amazônia com bico colorido impressionante.',
                'categoria': 'AVE',
                'estado_conservacao': 'VU',
                'regiao_brasil': 'Amazônia - Norte do Brasil',
                'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Ramphastos_vitellinus_-bird_avatar.jpg/800px-Ramphastos_vitellinus_-bird_avatar.jpg',
            },
            {
                'titulo': 'Harpia',
                'nome_cientifico': 'Harpia harpyja',
                'texto': 'Conhecida como gavião-real, uma das maiores aves de rapina.',
                'categoria': 'AVE',
                'estado_conservacao': 'VU',
                'regiao_brasil': 'Amazônia',
                'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Harpy_Eagle_%288356236590%29.jpg/800px-Harpy_Eagle_%288356236590%29.jpg',
            },
        ]
        
        try:
            user = User.objects.get(username='admin')
            animais_criados = 0
            
            for dados in animais:
                animal, created = AnimalRaro.objects.get_or_create(
                    titulo=dados['titulo'],
                    defaults={
                        'nome_cientifico': dados['nome_cientifico'],
                        'autor': user,
                        'texto': dados['texto'],
                        'categoria': dados['categoria'],
                        'estado_conservacao': dados['estado_conservacao'],
                        'regiao_brasil': dados['regiao_brasil'],
                        'imagem_url': dados['imagem_url'],
                    }
                )
                if created:
                    animal.publicar()
                    animais_criados += 1
                    self.stdout.write(f'   ✅ {dados["titulo"]}')
                else:
                    self.stdout.write(f'   ℹ️ {dados["titulo"]} (já existe)')
            
            self.stdout.write(self.style.SUCCESS(f'\n   📊 Total: {animais_criados} novos animais'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Erro nos animais: {e}'))
        
        # 3. RESUMO
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🎉 CONFIGURAÇÃO CONCLUÍDA!'))
        self.stdout.write('=' * 60)
        self.stdout.write('\n📋 RESUMO:')
        self.stdout.write(f'   • Usuários: {User.objects.count()}')
        self.stdout.write(f'   • Animais: {AnimalRaro.objects.count()}')
        self.stdout.write('\n🔗 PRÓXIMOS PASSOS:')
        self.stdout.write('   1. python manage.py runserver')
        self.stdout.write('   2. Acesse: http://127.0.0.1:8000/')
        self.stdout.write('   3. Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('=' * 60)