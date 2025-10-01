# usuario/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('redirect/', views.redirect_by_role, name='redirect_by_role'),
]

