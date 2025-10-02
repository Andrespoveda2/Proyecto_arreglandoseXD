from django.shortcuts import render
from usuario.utils import role_required

# --- Gestión (Admin) ---

@role_required("ADMIN")
def dashboard_admin(request):
    """Dashboard exclusivo para administradores."""
    return render(request, 'dashboard_admin.html')


@role_required("ADMIN")
def listar_usuarios(request):
    """Vista para listar y gestionar usuarios del sistema."""
    return render(request, 'listar_usuarios.html')


@role_required("ADMIN")
def gestion_programas(request):
    """Gestión de programas académicos o proyectos."""
    return render(request, 'gestion_programas.html')


@role_required("ADMIN")
def reportes(request):
    """Generación y visualización de reportes administrativos."""
    return render(request, 'reportes.html')
