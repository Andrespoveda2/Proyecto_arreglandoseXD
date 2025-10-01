from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_gestion(request):
    """Renderiza el dashboard específico para el rol de Gestión/Administrador."""
    # Nota: Los superusuarios tienen acceso al admin, pero esta es la vista para el rol de gestión.
    return render(request, 'gestion/dashboard.html')

@login_required
def gestionar_usuarios(request):
    """Placeholder: Herramientas para administrar usuarios y roles."""
    return HttpResponse("Página para gestionar usuarios (Gestión)")