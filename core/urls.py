# ARQUIVO: core/urls.py
# Substitua TODO o conteúdo do arquivo core/urls.py por este:

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('faturamento.urls')),
]