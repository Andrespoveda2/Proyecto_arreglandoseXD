from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_empresa(request):
    # Lógica: Obtener proyectos creados por esta empresa
    return render(request, 'empresas/dashboard_empresa.html')

@login_required
def crear_proyecto(request):
    return render(request, 'empresas/crear_proyecto.html')

@login_required
def editar_proyecto(request, pk):
    return render(request, 'empresas/editar_proyecto.html')