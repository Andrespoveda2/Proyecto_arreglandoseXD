from django.urls import path
from . import views

urlpatterns = [
    # Ruta principal del dominio (/)
    path('', views.index, name='inicio'), 
    path('acerca_de', views.acerca_de, name='acerca_de'),
]

