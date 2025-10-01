from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_aprendiz(request):
    """Renderiza el dashboard específico para el rol de Aprendiz."""
    return render(request, 'aprendices/dashboard.html')

@login_required
def ver_proyectos(request):
    """Placeholder para la función de ver proyectos disponibles."""
    return HttpResponse("Página para ver proyectos disponibles (Aprendiz)")

@login_required
def perfil_aprendiz(request):
    """Placeholder para la vista del perfil del aprendiz."""
    return HttpResponse("Página de Perfil (Aprendiz)")

@login_required
def detalle_proyecto(request, pk):
    """Mostrar detalles de un proyecto específico."""
    return HttpResponse(f"Detalle del proyecto con ID {pk} (Aprendiz)")

@login_required
def asignacion_list(request):
    """Listado de proyectos en los que el aprendiz se postuló o fue asignado."""
    return HttpResponse("Listado de asignaciones (Aprendiz)")
