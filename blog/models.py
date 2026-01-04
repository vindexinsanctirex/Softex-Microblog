# blog/models.py

from django.db import models
from django.utils import timezone

class AnimalRaro(models.Model):
    # Categorias de animais
    CATEGORIAS = [
        ('MAMIFERO', 'Mamífero'),
        ('AVE', 'Ave'),
        ('REPTIL', 'Réptil'),
        ('ANFIBIO', 'Anfíbio'),
        ('PEIXE', 'Peixe'),
        ('INSETO', 'Inseto'),
    ]
    
    # Estados de conservação
    ESTADO_CONSERVACAO = [
        ('CR', 'Criticamente em Perigo'),
        ('EM', 'Em Perigo'),
        ('VU', 'Vulnerável'),
        ('NT', 'Quase Ameaçada'),
        ('LC', 'Pouco Preocupante'),
    ]
    
    titulo = models.CharField(max_length=200)
    nome_cientifico = models.CharField(max_length=200)
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    texto = models.TextField()
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default='MAMIFERO')
    estado_conservacao = models.CharField(max_length=2, choices=ESTADO_CONSERVACAO, default='VU')
    regiao_brasil = models.CharField(max_length=100)
    imagem_url = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)
    publicado_em = models.DateTimeField(blank=True, null=True)
    
    def publicar(self):
        self.publicado_em = timezone.now()
        self.save()
    
    def __str__(self):
        return self.titulo