from django.shortcuts import render, get_object_or_404, redirect
from usuario.utils import role_required
from .models import AsignacionInstructor
from empresas.models import SolicitudProyecto
from .forms import SeguimientoForm

@role_required("INSTRUCTOR")
def dashboard_instructor(request):
    """Panel principal del instructor."""
    proyectos = AsignacionInstructor.objects.filter(instructor=request.user)
    return render(request, 'dashboard_instructor.html', {'proyectos': proyectos})

@role_required("INSTRUCTOR")
def proyectos_asignados(request):
    """Lista de proyectos asignados."""
    proyectos = AsignacionInstructor.objects.filter(instructor=request.user)
    return render(request, 'proyectos_asignados.html', {'proyectos': proyectos})

@role_required("INSTRUCTOR")
def seguimiento_avance(request, pk):
    """Editar el avance del proyecto asignado."""
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    form = SeguimientoForm(request.POST or None, instance=proyecto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('proyectos_asignados')
    return render(request, 'seguimiento_avance.html', {'form': form, 'proyecto': proyecto})

@role_required("INSTRUCTOR")
def perfil_instructor(request):
    """Ver perfil del instructor."""
    return render(request, 'perfil_instructor.html')
