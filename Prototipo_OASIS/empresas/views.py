from django.shortcuts import render
from django.http import HttpResponse
from usuario.utils import role_required

  # Ajusta la ruta según donde tengas el decorador

# --- EMPRESA ---

@role_required("EMPRESA")
def dashboard_empresa(request):
    """Renderiza el dashboard específico para el rol de Empresa."""
    return render(request, 'dashboard_empresa.html')


@role_required("EMPRESA")
def crear_proyecto(request):
    """Formulario para la creación de un nuevo proyecto."""
    return render(request, 'crear_proyecto.html')


@role_required("EMPRESA")
def editar_proyecto(request, pk):
    """Formulario para editar un proyecto específico por ID."""
    return render(request, 'editar_proyecto.html', {'proyecto_id': pk})


@role_required("EMPRESA")
def ver_solicitudes(request):
    """Página para visualizar las solicitudes recibidas."""
    return render(request, 'ver_solicitudes.html')
