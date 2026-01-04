# blog/admin.py

from django.contrib import admin
from .models import AnimalRaro

@admin.register(AnimalRaro)
class AnimalRaroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nome_cientifico', 'autor', 'categoria', 'estado_conservacao', 'publicado_em')
    list_filter = ('categoria', 'estado_conservacao', 'publicado_em')
    search_fields = ('titulo', 'nome_cientifico', 'texto')
    prepopulated_fields = {'titulo': ('nome_cientifico',)}