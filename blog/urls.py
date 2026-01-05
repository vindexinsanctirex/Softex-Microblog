# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_animais, name='lista_animais'),
    path('animal/<int:pk>/', views.detalhe_animal, name='detalhe_animal'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('categoria/<str:categoria>/', views.animais_por_categoria, name='animais_por_categoria'),
    path('emergency-fix/', views.emergency_fix, name='emergency_fix'), 
]