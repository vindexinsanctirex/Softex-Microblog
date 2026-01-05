# blog/views.py

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import AnimalRaro
from django.core.paginator import Paginator
from django.db.models import Q

def lista_animais(request):
    animais = AnimalRaro.objects.filter(publicado_em__lte=timezone.now()).order_by('-publicado_em')
    
    # Paginação
    paginator = Paginator(animais, 6)  # 6 animais por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/lista_animais.html', {'page_obj': page_obj})

def detalhe_animal(request, pk):
    animal = get_object_or_404(AnimalRaro, pk=pk)
    return render(request, 'blog/detalhe_animal.html', {'animal': animal})

def animais_por_categoria(request, categoria):
    animais = AnimalRaro.objects.filter(
        categoria=categoria,
        publicado_em__lte=timezone.now()
    ).order_by('-publicado_em')
    
    # Mapear códigos de categoria para nomes legíveis
    categorias_nomes = dict(AnimalRaro.CATEGORIAS)
    nome_categoria = categorias_nomes.get(categoria, categoria)
    
    return render(request, 'blog/categoria.html', {
        'animais': animais,
        'categoria': nome_categoria,
        'codigo_categoria': categoria
    })

def sobre(request):
    return render(request, 'blog/sobre.html')

def contato(request):
    if request.method == 'POST':
        # Aqui você pode processar o formulário de contato
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        
        # Em um projeto real, você enviaria um email aqui
        # Por enquanto, apenas exibiremos uma mensagem de sucesso
        sucesso = True
        
        return render(request, 'blog/contato.html', {'sucesso': sucesso})
    
    return render(request, 'blog/contato.html')

from django.http import HttpResponse
from django.contrib.auth.models import User
import os

def create_admin_now(request):
    """Endpoint para criar admin via navegador - REMOVER DEPOIS!"""
    
    # Senha de segurança (mude para algo seguro!)
    if request.GET.get('token') != 'animais123':
        return HttpResponse('🔒 Acesso negado', status=403)
    
    try:
        # Deletar admin antigo
        User.objects.filter(username='admin').delete()
        
        # Criar novo
        password = 'NovaSenhaSuperForte2024!'  # MUDE ESTA SENHA!
        email = 'admin@animaisraros.com'
        
        User.objects.create_superuser('admin', email, password)
        
        return HttpResponse(f'''
        <h1>✅ ADMIN CRIADO NO RENDER!</h1>
        
        <h3>📋 Credenciais:</h3>
        <p><strong>Usuário:</strong> admin</p>
        <p><strong>Senha:</strong> {password}</p>
        <p><strong>Email:</strong> {email}</p>
        
        <h3>🔗 Acesso:</h3>
        <p><a href="/admin/" target="_blank">➡️ Clique aqui para ir ao Admin</a></p>
        
        <h3>⚠️ IMPORTANTE:</h3>
        <p>1. Esta página deve ser REMOVIDA após usar</p>
        <p>2. Mude a senha no código acima</p>
        <p>3. Mude o token 'animais123' para algo mais seguro</p>
        ''')
        
    except Exception as e:
        return HttpResponse(f'❌ Erro: {str(e)}')