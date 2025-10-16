# Django imports
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Utils
from usuario.utils import role_required

# Models
from usuario.models import PerfilInstructor
from .models import AsignacionInstructor, InstructorProfile  # Evitar duplicado si ya lo importaste de usuario.models
from empresas.models import SolicitudProyecto, PostulacionInstructor

# Forms
from .forms import SeguimientoForm, InstructorProfileForm



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
def detalle_proyecto_instructor(request, pk):
    """Muestra el detalle de un proyecto y permite postularse como instructor guía."""
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    instructor = request.user.perfil_instructor
    ya_postulado = PostulacionInstructor.objects.filter(instructor=instructor, proyecto=proyecto).exists()

    return render(request, "detalle_proyecto_instructor.html", {
        "proyecto": proyecto,
        "ya_postulado": ya_postulado,
    })


@role_required("INSTRUCTOR")
def lista_proyectos(request):
    """Muestra todos los proyectos disponibles para postularse como instructor guía."""
    proyectos = SolicitudProyecto.objects.filter(estado="APROBADO")

@role_required("INSTRUCTOR")
def listar_proyectos(request):
    """Muestra todos los proyectos disponibles para que el instructor se postule."""
    proyectos = SolicitudProyecto.objects.filter(estado="APROBADO")
    return render(request, "listar_proyectos_instructor.html", {"proyectos": proyectos})


@role_required("INSTRUCTOR")
def seguimiento_avance(request, pk):
    """Editar el avance del proyecto asignado."""
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    form = SeguimientoForm(request.POST or None, instance=proyecto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Avance del proyecto actualizado correctamente.")
        return redirect('proyectos_asignados')
    return render(request, 'seguimiento_avance.html', {'form': form, 'proyecto': proyecto})

@role_required("INSTRUCTOR")
def editar_perfil_instructor(request):
    """
    Permite al usuario logueado editar o crear su perfil de instructor.
    """
    
    # Intentamos obtener el perfil existente. Si no existe, lo creamos.
    # Usamos get_or_create, lo que garantiza que la instancia siempre existe aquí.
    perfil_instance, created = PerfilInstructor.objects.get_or_create(
        usuario=request.user,
        # Si se crea, establecemos valores por defecto para campos obligatorios
        defaults={'numero_identificacion': f'TEMP-{request.user.id}'} 
    )

    if created:
        messages.info(request, "¡Bienvenido, instructor! Por favor, completa tu perfil para continuar.")
    
    if request.method == 'POST':
        # Pasamos request.FILES para la foto y la instancia para actualizar.
        form = InstructorProfileForm(request.POST, request.FILES, instance=perfil_instance)
        
        if form.is_valid():
            perfil_guardado = form.save(commit=False)
            perfil_guardado.usuario = request.user
            perfil_guardado.save()
            
            messages.success(request, "Tu perfil de instructor ha sido actualizado exitosamente.")

            # Redirigir a la vista de perfil del instructor (usando la ruta simple)
            return redirect('instructores:mi_perfil_instructor')
        
        messages.error(request, "Hubo errores en el formulario. Por favor, revísalos e inténtalo de nuevo.")

    else:
        # Petición GET: Cargamos el formulario con los datos actuales.
        form = InstructorProfileForm(instance=perfil_instance)

    context = {
        'form': form,
        'perfil_instance': perfil_instance 
    }
    
    # CORRECCIÓN DE NOMBRE DE TEMPLATE para evitar conflicto. 
    # El archivo HTML DEBE llamarse 'instructor_form_edit.html'
    return render(request, 'perfil_form.html', context)


# VISTA PARA MOSTRAR EL PERFIL
@role_required("INSTRUCTOR")
def perfil_instructor(request, perfil_id=None): 
    """
    Muestra el perfil de un instructor. Si perfil_id es None, muestra el perfil del usuario logueado.
    """
    if perfil_id:
        # Caso 1: Se proporciona un ID (ver perfil de otro)
        perfil = get_object_or_404(PerfilInstructor, pk=perfil_id)
    else:
        # Caso 2: URL simple (/perfil/), buscar el perfil del usuario logueado.
        try:
            perfil = PerfilInstructor.objects.get(usuario=request.user)
        except PerfilInstructor.DoesNotExist:
            # Si el usuario logueado NO tiene perfil, lo enviamos inmediatamente a crearlo.
            messages.warning(request, "Aún no tienes un perfil de instructor creado. ¡Vamos a crearlo!")
            # Redirigir al URL de edición
            return redirect('instructores:editar_perfil_instructor')


    context = {
        'perfil': perfil,
        # Útil para saber si el usuario logueado está viendo SU perfil.
        'es_propietario': perfil.usuario == request.user 
    }
    
    # Nombre de template para visualizar el perfil
    return render(request, 'perfil_instructor.html', context)

@role_required("INSTRUCTOR")
def postular_proyecto_instructor(request, pk):
    """Permite al instructor postularse como guía de un proyecto."""
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    instructor = request.user.perfil_instructor

    postulacion_existente = PostulacionInstructor.objects.filter(instructor=instructor, proyecto=proyecto).exists()
    if postulacion_existente:
        messages.warning(request, "⚠️ Ya te postulaste a este proyecto.")
        return redirect('instructores:detalle_proyecto_instructor', pk=proyecto.id)

    PostulacionInstructor.objects.create(instructor=instructor, proyecto=proyecto)
    messages.success(request, f"✅ Te has postulado como instructor guía para '{proyecto.nombre}'.")
    return redirect('instructores:detalle_proyecto_instructor', pk=proyecto.id)
