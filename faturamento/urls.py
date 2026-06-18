# ARQUIVO: faturamento/urls.py
# Crie este arquivo em faturamento/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Clientes
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_criar, name='cliente_criar'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/excluir/', views.cliente_excluir, name='cliente_excluir'),

    # Faturas
    path('faturas/', views.fatura_lista, name='fatura_lista'),
    path('faturas/<int:pk>/', views.fatura_detalhe, name='fatura_detalhe'),
    path('faturas/nova/', views.fatura_criar, name='fatura_criar'),
    path('faturas/<int:pk>/editar/', views.fatura_editar, name='fatura_editar'),
    path('faturas/<int:pk>/excluir/', views.fatura_excluir, name='fatura_excluir'),
]