from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from usuario.utils import role_required
from .forms import SolicitudProyectoForm
from .models import SolicitudProyecto
from usuario.models import PerfilEmpresa


@role_required("EMPRESA")
def dashboard_empresa(request):
    empresa = request.user.perfil_empresa
    proyectos = SolicitudProyecto.objects.filter(empresa=empresa)
    return render(request, 'dashboard_empresa.html', {'proyectos': proyectos})


@role_required("EMPRESA")
def crear_proyecto(request):
    empresa = request.user.perfil_empresa
    if request.method == 'POST':
        form = SolicitudProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.empresa = empresa
            proyecto.estado = "PENDIENTE"
            proyecto.save()
            messages.success(request, "✅ Proyecto creado correctamente.")
            return redirect('empresas:dashboard_empresa')
    else:
        form = SolicitudProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})


@role_required("EMPRESA")
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk, empresa=request.user.perfil_empresa)
    if request.method == 'POST':
        form = SolicitudProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Proyecto actualizado correctamente.")
            return redirect('empresas:dashboard_empresa')
    else:
        form = SolicitudProyectoForm(instance=proyecto)
    return render(request, 'editar_proyecto.html', {'form': form})

@role_required("EMPRESA")
def ver_solicitudes(request):
    """Página para visualizar las solicitudes recibidas."""
    return render(request, 'ver_solicitudes.html')

@role_required("EMPRESA")
def perfil_empresa(request):
    """Muestra el perfil de la empresa logueada."""
    empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
    return render(request, 'perfil_empresa.html', {'empresa': empresa})