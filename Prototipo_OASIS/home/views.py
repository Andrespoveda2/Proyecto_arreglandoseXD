from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """Renderiza la página de inicio (landing page)."""
    return render(request, 'home/index.html')

def acerca_de(request):
    """Renderiza la página 'Acerca de Nosotros'."""
    return render(request, 'home/acerca_de_nosotros.html')
