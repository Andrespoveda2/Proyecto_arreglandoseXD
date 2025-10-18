from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Decoradores y modelos de usuario
from usuario.utils import role_required
from usuario.models import PerfilEmpresa

# Modelos y formularios de la app empresas
from .models import SolicitudProyecto, Postulacion, PostulacionInstructor, SolicitudProyecto, Empresa
from .forms import SolicitudProyectoForm, EmpresaProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView




@role_required("EMPRESA")
def dashboard_empresa(request):
    empresa = request.user.perfil_empresa
    proyectos = SolicitudProyecto.objects.filter(empresa=empresa)
    return render(request, 'dashboard_empresa.html', {'proyectos': proyectos})

@role_required("EMPRESA")
def editar_perfil_empresa(request):
    """
    Permite al usuario logueado con rol de empresa editar o crear su perfil.
    """
    
    # 1. Intentamos obtener el perfil existente o crear uno temporal.
    perfil_instance, created = PerfilEmpresa.objects.get_or_create(
        usuario=request.user,
        # Establecemos valores por defecto para campos obligatorios si es una creación
        defaults={'nit': f'TEMP-{request.user.id}', 'razon_social': 'Empresa Temporal'} 
    )

    if created:
        messages.info(request, "¡Bienvenido! Por favor, completa el perfil de tu empresa para empezar a crear proyectos.")
    
    if request.method == 'POST':
        # Pasamos request.FILES para la foto/logo y la instancia para actualizar.
        form = EmpresaProfileForm(request.POST, request.FILES, instance=perfil_instance)
        
        if form.is_valid():
            perfil_guardado = form.save(commit=False)
            perfil_guardado.usuario = request.user
            perfil_guardado.save()
            
            messages.success(request, "El perfil de tu empresa ha sido actualizado exitosamente.")

            # Redirigir a la vista de visualización del perfil
            return redirect('empresas:mi_perfil_empresa') # <- Asegúrate que el name sea correcto
        
        messages.error(request, "Hubo errores en el formulario. Por favor, revísalos e inténtalo de nuevo.")

    else:
        # Petición GET: Cargamos el formulario con los datos actuales.
        form = EmpresaProfileForm(instance=perfil_instance)

    context = {
        'form': form,
        'perfil_instance': perfil_instance 
    }
    
    # Template de edición de empresa (usando 'empresa_form_edit.html' para evitar conflictos)
    return render(request, 'editar_perfil.html', context)


@role_required("EMPRESA")
def Perfil_Empresa(request, empresa_id=None):
    """
    Muestra el perfil de una empresa. Si empresa_id es None, muestra el perfil del usuario logueado.
    """
    if empresa_id:
        # Caso 1: Ver perfil de otra empresa (URL dinámica)
        perfil = get_object_or_404(PerfilEmpresa, pk=empresa_id)
        
    else:
        # Caso 2: Ver perfil propio (URL estática: /empresa/perfil/)
        try:
            # Aquí es donde fallaba antes si el perfil no existía:
            perfil = PerfilEmpresa.objects.get(usuario=request.user)
            
        except PerfilEmpresa.DoesNotExist:
            # 💡 SOLUCIÓN: Si no existe, NO lanzamos un 404, redirigimos a la edición.
            messages.warning(request, "Tu perfil de empresa aún no está completo. Por favor, rellena los datos.")
            return redirect('empresas:editar_perfil_empresa')


    context = {
        'perfil': perfil,
        # Útil para saber si el usuario logueado está viendo SU perfil.
        'es_propietario': perfil.usuario == request.user if perfil else False
    }
    
    # Nombre de template para visualizar el perfil (asumimos que ya lo tienes)
    return render(request, 'perfil_empresa.html', context)



@role_required("EMPRESA")
def crear_proyecto(request):
    empresa = request.user.perfil_empresa
    if request.method == 'POST':
        form = SolicitudProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            # ✅ Asignamos automáticamente la empresa logueada
            proyecto.empresa = empresa  
            # ✅ Estado inicial
            proyecto.estado = "PENDIENTE"
            proyecto.save()
            messages.success(request, "✅ Tu solicitud de proyecto fue enviada para revisión.")
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
def postulaciones_proyecto(request, pk):
    empresa = request.user.perfil_empresa
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk, empresa=empresa)
    postulaciones = Postulacion.objects.filter(proyecto=proyecto)

    return render(request, 'postulaciones_proyectos.html', {
        'proyecto': proyecto,
        'postulaciones': postulaciones
    })

@role_required("EMPRESA")
def gestionar_postulacion(request, postulacion_id, accion):
    """
    Permite aceptar o rechazar una postulación.
    - accion = 'aceptar' o 'rechazar'
    """
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    proyecto = postulacion.proyecto
    aprendiz = postulacion.aprendiz

    # Validación de permisos
    if proyecto.empresa != request.user.perfil_empresa:
        messages.error(request, "❌ No tienes permisos para realizar esta acción.")
        return redirect('empresas:dashboard_empresa')

    if postulacion.estado != "PENDIENTE":
        messages.warning(request, "⚠️ Esta postulación ya fue procesada.")
        return redirect('empresas:postulaciones_proyecto', pk=proyecto.id)

    if accion == "aceptar":
        postulacion.estado = "ACEPTADA"
        postulacion.save()

        # 🔹 Añadir el proyecto al perfil del aprendiz
        aprendiz.proyectos_asignados.add(proyecto)

        messages.success(request, f"✅ {aprendiz.usuario.username} ha sido aceptado para el proyecto '{proyecto.nombre}'.")

    elif accion == "rechazar":
        postulacion.estado = "RECHAZADA"
        postulacion.save()
        messages.info(request, f"❌ {aprendiz.usuario.username} ha sido rechazado para el proyecto '{proyecto.nombre}'.")

    else:
        messages.warning(request, "⚠️ Acción no válida.")

    return redirect('empresas:postulaciones_proyecto', pk=proyecto.id)

@role_required("EMPRESA")
def gestionar_postulacion_instructor(request, postulacion_id, accion):
    """
    Permite aceptar o rechazar una postulación de instructor guía.
    """
    postulacion = get_object_or_404(PostulacionInstructor, id=postulacion_id)
    proyecto = postulacion.proyecto

    # Validar que la empresa sea dueña del proyecto
    if proyecto.empresa != request.user.perfil_empresa:
        messages.error(request, "❌ No tienes permisos para realizar esta acción.")
        return redirect('empresas:dashboard_empresa')

    if postulacion.estado != "PENDIENTE":
        messages.warning(request, "⚠️ Esta postulación ya fue procesada.")
        return redirect('empresas:postulaciones_proyecto', pk=proyecto.id)

    if accion == "aceptar":
        postulacion.estado = "ACEPTADA"
        postulacion.save()
        # Asignar instructor guía al proyecto
        proyecto.instructor = postulacion.instructor
        proyecto.save()
        messages.success(request, f"✅ {postulacion.instructor.usuario.username} ha sido asignado como instructor guía del proyecto '{proyecto.nombre}'.")

    elif accion == "rechazar":
        postulacion.estado = "RECHAZADA"
        postulacion.save()
        messages.info(request, f"❌ Has rechazado a {postulacion.instructor.usuario.username} como instructor guía.")

    else:
        messages.warning(request, "⚠️ Acción no válida.")

    return redirect('empresas:postulaciones_proyecto', pk=proyecto.id)

def detalle_proyecto_empresa(request, pk):
    # Obtener el proyecto específico
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)

    # Obtener las relaciones directas
    instructor = proyecto.instructor  # puede ser None
    aprendices = proyecto.aprendices.all()  # queryset, puede estar vacío

    context = {
        'proyecto': proyecto,
        'instructor': instructor,
        'aprendices': aprendices,
    }
    return render(request, 'detalle_proyecto_empresa.html', context)

class DetalleSolicitudProyectoView(LoginRequiredMixin, DetailView):
    model = SolicitudProyecto
    template_name = 'detalle_solicitud.html'
    context_object_name = 'solicitud'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        user = self.request.user
        try:
            perfil_empresa = user.perfil_empresa
            return SolicitudProyecto.objects.filter(empresa=perfil_empresa)
        except:
            return SolicitudProyecto.objects.none()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Los campos motivo_aprobacion y motivo_rechazo ya están 
        # directamente en el objeto solicitud
        solicitud = self.get_object()
        context['motivo_aprobacion'] = solicitud.motivo_aprobacion
        context['motivo_rechazo'] = solicitud.motivo_rechazo
        context['estado'] = solicitud.estado
        context['fecha_decision'] = solicitud.fecha_decision
        return context