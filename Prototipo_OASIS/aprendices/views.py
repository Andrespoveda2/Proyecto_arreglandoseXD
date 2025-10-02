from django.shortcuts import render
from usuario.utils import role_required

# --- APRENDIZ ---

@role_required("APRENDIZ")
def dashboard_aprendiz(request):
    """Renderiza el dashboard específico para el rol de Aprendiz."""
    return render(request, 'dashboard_aprendiz.html')

@role_required("APRENDIZ")
def ver_proyectos(request):
    """Ver proyectos disponibles para el aprendiz."""
    return render(request, 'proyectos_disponibles.html')

@role_required("APRENDIZ")
def perfil_aprendiz(request):
    """Vista del perfil del aprendiz."""
    return render(request, 'perfil_aprendiz.html')

@role_required("APRENDIZ")
def detalle_proyecto(request, pk):
    """Mostrar detalles de el proyecto específico al que esta asignado el aprendiz."""
    return render(request, 'detalle_proyecto.html', {'proyecto_id': pk})
