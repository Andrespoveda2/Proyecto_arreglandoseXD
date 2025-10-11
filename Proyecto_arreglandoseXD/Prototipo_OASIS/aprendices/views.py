from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from usuario.utils import role_required
from usuario.models import PerfilAprendiz
from empresas.models import SolicitudProyecto
from .models import Postulacion

# --- APRENDIZ ---

@role_required("APRENDIZ")
def dashboard_aprendiz(request):
    """Panel principal del aprendiz: muestra sus proyectos asignados y postulaciones."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)
    
    postulaciones = Postulacion.objects.filter(aprendiz=aprendiz)
    proyectos_asignados = aprendiz.proyectos_asignados.all()  # desde el ManyToMany de SolicitudProyecto

    return render(request, 'dashboard_aprendiz.html', {
        'aprendiz': aprendiz,
        'proyectos_asignados': proyectos_asignados,
        'postulaciones': postulaciones,
    })


@role_required("APRENDIZ")
def ver_proyectos(request):
    """Muestra proyectos disponibles según el programa formativo del aprendiz."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)

    proyectos = SolicitudProyecto.objects.filter(
        programa_formativo=aprendiz.programa,
        estado="APROBADO"
    ).exclude(postulaciones__aprendiz=aprendiz)

    return render(request, 'proyectos_disponibles.html', {
        'aprendiz': aprendiz,
        'proyectos': proyectos
    })


@role_required("APRENDIZ")
def postular_proyecto(request, pk):
    """Permite al aprendiz postularse a un proyecto."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)

    # Verificar si ya se postuló
    if Postulacion.objects.filter(aprendiz=aprendiz, proyecto=proyecto).exists():
        messages.warning(request, "Ya te has postulado a este proyecto.")
    else:
        Postulacion.objects.create(aprendiz=aprendiz, proyecto=proyecto)
        messages.success(request, "Tu postulación fue enviada correctamente.")

    return redirect('aprendices:ver_proyectos')  # ✅ corregido con namespace


@role_required("APRENDIZ")
def detalle_proyecto(request, pk):
    """Muestra los detalles de un proyecto específico."""
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    return render(request, 'detalle_proyecto.html', {
        'proyecto': proyecto
    })


@role_required("APRENDIZ")
def perfil_aprendiz(request):
    """Muestra el perfil del aprendiz logueado."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)
    return render(request, 'perfil_aprendiz.html', {
        'aprendiz': aprendiz
    })
