from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_aprendiz(request):
    """Renderiza el dashboard específico para el rol de Aprendiz."""
    return render(request, 'aprendices/dashboard.html')

def ver_proyectos(request):
    """Placeholder para la función de ver proyectos."""
    return HttpResponse("Página para ver proyectos disponibles (Aprendiz)")

def perfil_aprendiz(request):
    """Placeholder para la vista del perfil del aprendiz."""
    return HttpResponse("Página de Perfil (Aprendiz)")