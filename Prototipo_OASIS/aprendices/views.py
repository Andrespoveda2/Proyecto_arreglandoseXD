from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from usuario.utils import role_required
from usuario.models import PerfilAprendiz
from usuario.forms import PerfilAprendizForm # Importamos el formulario correcto
from empresas.models import SolicitudProyecto, Postulacion

# --- APRENDIZ ---

@role_required("APRENDIZ")
def dashboard_aprendiz(request):
    """Panel principal del aprendiz: muestra sus proyectos asignados y postulaciones."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)

    # 🔹 Proyectos en los que el aprendiz ya está asignado
    proyectos_asignados = SolicitudProyecto.objects.filter(aprendices=aprendiz)

    # 🔹 Postulaciones realizadas (proyectos a los que se ha postulado)
    postulaciones = aprendiz.postulaciones_proyecto.select_related("proyecto")

    # 🔹 Extraer los proyectos de las postulaciones
    proyectos_postulados = [p.proyecto for p in postulaciones]

    # 🔹 Unir ambos sin duplicados
    proyectos = list({p.id: p for p in list(proyectos_asignados) + proyectos_postulados}.values())

    # 🔹 Obtener lista de IDs de proyectos donde ya está postulado (para usar en el template)
    postulaciones_ids = list(postulaciones.values_list("proyecto__id", flat=True))

    return render(request, 'dashboard_aprendiz.html', {
        'aprendiz': aprendiz,
        'proyectos': proyectos,          # ✅ lista de proyectos combinada
        'postulaciones': postulaciones,  # ✅ sigue disponible por si la usas en otro bloque
        'postulaciones_ids': postulaciones_ids,  # ✅ nueva lista simple para el {% if %}
    })


@role_required("APRENDIZ")
def ver_proyectos(request):
    """Muestra proyectos disponibles según el programa formativo del aprendiz."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)

    proyectos = SolicitudProyecto.objects.filter(
        programa_formativo=aprendiz.programa,
        estado="APROBADO"
    ).exclude(postulaciones_aprendices__aprendiz=aprendiz)  # CORRECTO, según tu modelo

    return render(request, 'proyectos_disponibles.html', {
        'aprendiz': aprendiz,
        'proyectos': proyectos
    })


@role_required("APRENDIZ")
def detalle_proyecto(request, pk):
    """Muestra los detalles del proyecto y si el aprendiz ya se postuló."""
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk, estado="APROBADO")
    aprendiz = request.user.perfil_aprendiz  # igual que en postular_proyecto

    # Verificar si ya está postulado
    ya_postulado = Postulacion.objects.filter(aprendiz=aprendiz, proyecto=proyecto).exists()

    # Verificar si el programa formativo coincide
    programa_coincide = (proyecto.programa_formativo == aprendiz.programa)

    context = {
        'proyecto': proyecto,
        'ya_postulado': ya_postulado,
        'programa_coincide': programa_coincide,
    }
    return render(request, 'detalle_proyecto_aprendiz.html', context)


@role_required("APRENDIZ")
def perfil_aprendiz(request):
    """Muestra el perfil del aprendiz logueado."""
    aprendiz = get_object_or_404(PerfilAprendiz, usuario=request.user)
    return render(request, 'perfil_aprendiz.html', {
        'aprendiz': aprendiz
    })


@role_required("APRENDIZ")
def editar_perfil_aprendiz(request):
    """
    Vista para editar el perfil del Aprendiz (Modelo PerfilAprendiz).
    """
    try:
        aprendiz_profile = get_object_or_404(PerfilAprendiz, usuario=request.user)
    except PerfilAprendiz.DoesNotExist:
        messages.error(request, "No se encontró un perfil de aprendiz asociado a tu cuenta.")
        return redirect('aprendices:dashboard_aprendiz')
        
    if request.method == 'POST':
        # Instanciar el formulario con los datos POST y la instancia del perfil
        form = PerfilAprendizForm(request.POST, instance=aprendiz_profile)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('aprendices:perfil_aprendiz')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        # Si es GET, instanciar el formulario con los datos existentes
        form = PerfilAprendizForm(instance=aprendiz_profile)
        
    context = {
        'form': form,
        'aprendiz': aprendiz_profile,
    }
    return render(request, 'editar_perfil_aprendiz.html', context)

@role_required("APRENDIZ")
def postular_proyecto(request, pk):
    """Permite a un aprendiz postularse a un proyecto disponible."""
    aprendiz = request.user.perfil_aprendiz  # CORRECTO
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk, estado="APROBADO")

    # Validar que el proyecto corresponda a su programa
    if proyecto.programa_formativo != aprendiz.programa:
        messages.warning(request, "⚠️ Este proyecto no corresponde a tu programa formativo.")
        return redirect('aprendices:ver_proyectos')

    # Verificar si ya está postulado
    if Postulacion.objects.filter(aprendiz=aprendiz, proyecto=proyecto).exists():
        messages.info(request, "ℹ️ Ya estás postulado a este proyecto.")
        return redirect('aprendices:ver_proyectos')

    # Crear la postulación
    Postulacion.objects.create(aprendiz=aprendiz, proyecto=proyecto)
    messages.success(request, f"✅ Te has postulado correctamente al proyecto '{proyecto.nombre}'.")
    return redirect('aprendices:ver_proyectos')