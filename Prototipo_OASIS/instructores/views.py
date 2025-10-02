from django.shortcuts import render
from usuario.utils import role_required  # Importamos el decorador centralizado

# --- INSTRUCTOR ---

@role_required("INSTRUCTOR")
def dashboard_instructor(request):
    """Dashboard exclusivo para instructores."""
    return render(request, 'dashboard.html')  


@role_required("INSTRUCTOR")
def proyectos_asignados(request):
    """Ver proyectos asignados al instructor."""
    return render(request, 'proyectos_asignados.html')


@role_required("INSTRUCTOR")
def seguimiento_avance(request, pk):
    """Ver o editar el avance de un proyecto específico."""
    return render(request, 'seguimiento_avance.html', {'proyecto_id': pk})

   
