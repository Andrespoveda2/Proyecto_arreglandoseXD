from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='inicio'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    path('tyc/', views.tyc, name='tyc'),  # Términos y Condiciones
    path('pdp/', views.Policy_Data_Protection, name='Policy_Data_Protection'),  # Política de Privacidad
]
