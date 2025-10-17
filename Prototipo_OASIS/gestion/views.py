from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.db.models import Count
from django.contrib.auth.mixins import UserPassesTestMixin

# Decoradores y modelos/funciones de usuario
from usuario.utils import role_required
from usuario.models import Usuario, ProgramaFormativo, SectorProductivo
from usuario.forms import ProgramaFormativoForm, SectorProductivoForm

# Formularios propios de la app gestión
from .forms import UsuarioForm

# Modelos externos relacionados
from empresas.models import SolicitudProyecto
from django.views.decorators.http import require_POST, require_http_methods
from empresas.models import SolicitudProyecto

# --- Vistas del Dashboard y Métricas ---

class DetalleUsuarioView(UserPassesTestMixin, DetailView):
    model = Usuario
    template_name = 'detalle_usuario.html'
    context_object_name = 'usuario_seleccionado' # Cambiamos el nombre para ser consistentes

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'ADMIN' #type: ignore

    def get_context_data(self, **kwargs):
        """
        Añade el perfil específico del usuario al contexto.
        """
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()
        perfil = None

        try:
            if usuario.rol == Usuario.APRENDIZ:
                perfil = usuario.perfil_aprendiz
            elif usuario.rol == Usuario.INSTRUCTOR:
                perfil = usuario.perfil_instructor
            elif usuario.rol == Usuario.EMPRESA:
                perfil = usuario.perfil_empresa
        except (
            Usuario.perfil_aprendiz.RelatedObjectDoesNotExist,
            Usuario.perfil_instructor.RelatedObjectDoesNotExist,
            Usuario.perfil_empresa.RelatedObjectDoesNotExist
        ):
            pass

        context['perfil'] = perfil
        return context
        
@role_required("ADMIN")
def dashboard_admin(request):
    """
    Dashboard exclusivo para administradores, consolidando métricas clave.
    """
    # 1. Conteo de Usuarios Totales
    total_usuarios = Usuario.objects.count()

    # 2. Conteo de Usuarios por Rol
    usuarios_por_rol = {
        'admins': Usuario.objects.filter(rol=Usuario.ADMIN).count(),
        'instructores': Usuario.objects.filter(rol=Usuario.INSTRUCTOR).count(),
        'empresas': Usuario.objects.filter(rol=Usuario.EMPRESA).count(),
        'aprendices': Usuario.objects.filter(rol=Usuario.APRENDIZ).count(),
    }
    
    # 3. Usuarios Recientes (últimos 5)
    usuarios_recientes = Usuario.objects.order_by('-date_joined')[:5]

    # 4. Proyectos Pendientes (Asume que existe un modelo 'Proyecto' con estado 'PENDIENTE')
    # Si el modelo Proyecto no existe, mantendremos un valor constante por ahora
    try:
        # Intenta obtener el modelo Proyecto si está importado o definido.
        # Por ahora, usamos un valor hardcodeado como simulación.
        proyectos_pendientes_count = 8 
        # Si tuvieras el modelo: proyectos_pendientes_count = Proyecto.objects.filter(estado='PENDIENTE').count()
    except Exception:
        proyectos_pendientes_count = 0 


    context = {
        'user': request.user,
        'total_usuarios': total_usuarios,
        'usuarios_por_rol': usuarios_por_rol,
        'usuarios_recientes': usuarios_recientes,
        'proyectos_pendientes_count': proyectos_pendientes_count,
    }
    return render(request, 'dashboard_admin.html', context)


# --- Gestión de Usuarios (CRUD) ---

@role_required("ADMIN")
def listar_usuarios(request):
    """Vista para listar y gestionar usuarios del sistema con paginación y filtros."""
    buscar = request.GET.get('buscar', '')
    rol = request.GET.get('rol', '')

    usuarios = Usuario.objects.all()

    if buscar:
        usuarios = usuarios.filter(username__icontains=buscar)

    if rol:
        usuarios = usuarios.filter(rol=rol)

    usuarios = usuarios.order_by('-date_joined')
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    usuarios_paginados = paginator.get_page(page_number)

    context = {
        'usuarios': usuarios_paginados,
        'buscar_actual': buscar,
        'rol_actual': rol,
        'roles': Usuario.ROLES,
    }
    return render(request, 'listar_usuarios.html', context)

@role_required("ADMIN")
def crear_usuario(request):
    """Maneja la creación de nuevos usuarios."""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            # Deberías añadir un mensaje de éxito aquí
            return redirect('gestion:listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

@role_required("ADMIN")
def editar_usuario(request, pk):
    """Maneja la edición de un usuario existente."""
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Solo actualiza la contraseña si el campo no está vacío
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            # Deberías añadir un mensaje de éxito aquí
            return redirect('gestion:listar_usuarios')
    else:
        # Al editar, no hacemos que el campo de contraseña sea obligatorio
        form = UsuarioForm(instance=usuario)
        form.fields['password'].required = False 
    return render(request, 'editar_usuario.html', {'form': form})

@role_required("ADMIN")
def eliminar_usuario(request, pk):
    """Maneja la eliminación de un usuario."""
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        # Deberías añadir un mensaje de éxito aquí
        return redirect('gestion:listar_usuarios')
    # Muestra una página de confirmación antes de la eliminación real
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})


# --- Gestión de Programas y Sectores ---

@role_required("ADMIN") # Agregado el decorador de seguridad
def gestion_programas(request):
    """Maneja la creación y listado de Programas Formativos."""
    if request.method == "POST":
        form = ProgramaFormativoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:gestion_programas')
    else:
        form = ProgramaFormativoForm()

    programas = ProgramaFormativo.objects.all().order_by('nombre')

    return render(request, 'gestion_programas.html', {
        'form': form,
        'programas': programas,
    })

@role_required("ADMIN")
def editar_programa(request, pk):
    """Maneja la edición de un Programa Formativo existente."""
    programa = get_object_or_404(ProgramaFormativo, pk=pk)
    if request.method == 'POST':
        form = ProgramaFormativoForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            # messages.success(request, f"El programa '{programa.nombre}' ha sido actualizado.")
            return redirect('gestion:gestion_programas')
    else:
        # Para la edición, creamos el formulario con la instancia del programa.
        form = ProgramaFormativoForm(instance=programa)
    
    # Necesitamos una nueva plantilla para el formulario de edición.
    return render(request, 'editar_programa.html', {
        'form': form,
        'programa': programa
    })

@role_required("ADMIN")
def eliminar_programa(request, pk):
    """Maneja la eliminación de un Programa Formativo."""
    programa = get_object_or_404(ProgramaFormativo, pk=pk)
    programa.delete()
    # messages.success(request, f"El programa '{programa.nombre}' ha sido eliminado.")
    return redirect('gestion:gestion_programas')

@role_required("ADMIN") # Agregado el decorador de seguridad
def gestion_sectores(request):
    """Maneja la creación y listado de Sectores Productivos."""
    if request.method == "POST":
        form = SectorProductivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion:gestion_sectores')
    else:
        form = SectorProductivoForm()

    sectores = SectorProductivo.objects.all().order_by('nombre')

    return render(request, 'gestion_sectores.html', {
        'form': form,
        'sectores': sectores,
    })

@role_required("ADMIN")
def editar_sector(request, pk):
    """Maneja la edición de un Sector Productivo existente."""
    sector = get_object_or_404(SectorProductivo, pk=pk)
    if request.method == 'POST':
        form = SectorProductivoForm(request.POST, instance=sector)
        if form.is_valid():
            form.save()
            # messages.success(request, f"El sector '{sector.nombre}' ha sido actualizado.")
            return redirect('gestion:gestion_sectores')
    else:
        form = SectorProductivoForm(instance=sector)
    
    return render(request, 'editar_sector.html', {
        'form': form,
        'sector': sector
    })

@role_required("ADMIN")
def eliminar_sector(request, pk):
    """Maneja la eliminación de un Sector Productivo."""
    sector = get_object_or_404(SectorProductivo, pk=pk)
    # Para ser más seguro, esto debería ser un método POST con confirmación.
    # Por ahora, se mantiene simple para que coincida con la implementación de programas.
    # messages.success(request, f"El sector '{sector.nombre}' ha sido eliminado.")
    sector.delete()
    return redirect('gestion:gestion_sectores')

    
# --- Gestión de Proyectos ---

@role_required("ADMIN")
def proyectos_pendientes(request):
    """
    Vista que lista los proyectos que requieren aprobación administrativa.
    Asume que tienes un modelo 'Proyecto' disponible.
    """
    # Aquí iría la consulta a tu base de datos:
    # proyectos = Proyecto.objects.filter(estado='PENDIENTE').order_by('fecha_solicitud')
    
    # Placeholder: Datos de ejemplo para la vista
    proyectos_mock = [
        {'id': 1, 'nombre': 'App de Gestión de Inventario', 'solicitante': 'Empresa ABC', 'fecha': '2025-10-01'},
        {'id': 2, 'nombre': 'Sistema de Monitoreo IoT', 'solicitante': 'Instructor Juan', 'fecha': '2025-10-05'},
    ]
    
    context = {
        'proyectos': proyectos_mock,
    }
    
    return render(request, 'proyectos_pendientes.html', context)


# --- Reportes y Analíticas ---

@role_required("ADMIN")
def reportes(request):
    """Generación y visualización de reportes administrativos."""
    total_usuarios = Usuario.objects.count()

    usuarios_por_rol = {
        'admins': Usuario.objects.filter(rol=Usuario.ADMIN).count(),
        'instructores': Usuario.objects.filter(rol=Usuario.INSTRUCTOR).count(),
        'empresas': Usuario.objects.filter(rol=Usuario.EMPRESA).count(),
        'aprendices': Usuario.objects.filter(rol=Usuario.APRENDIZ).count(),
    }

    context = {
        'total_usuarios': total_usuarios,
        'usuarios_por_rol': usuarios_por_rol,
        # Aquí podrías añadir más datos para gráficos:
        # 'proyectos_por_sector': SectorProductivo.objects.annotate(count=Count('proyecto')).order_by('-count')
    }

    return render(request, 'reportes.html', context)

@role_required("ADMIN")
def revisar_solicitudes(request):
    """Muestra todos los proyectos en estado Pendiente con mejor diseño."""
    pendientes = SolicitudProyecto.objects.filter(estado="PENDIENTE").order_by('-creado_en')
    
    context = {
        'pendientes': pendientes,
    }
    
    return render(request, 'revisar_solicitudes.html', context)


@role_required("ADMIN")
@require_http_methods(["POST"])
def aprobar_proyecto(request, pk):
    """
    Aprueba un proyecto y lo deja disponible para los aprendices.
    Ahora guarda el motivo de aprobación en la BD.
    """
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    
    # Obtener el motivo de aprobación del formulario
    motivo_aprobacion = request.POST.get('motivo_aprobacion', '').strip()
    
    # Validar que el motivo no esté vacío
    if not motivo_aprobacion:
        messages.error(request, "⚠️ Debes proporcionar un motivo para la aprobación.")
        return redirect('gestion:revisar_solicitudes')
    
    # Actualizar el proyecto
    proyecto.estado = "APROBADO"
    proyecto.motivo_aprobacion = motivo_aprobacion
    proyecto.save()
    
    # Mensaje de éxito
    messages.success(
        request, 
        f"✅ Proyecto '{proyecto.nombre}' ha sido aprobado. "
        f"La empresa ha sido notificada."
    )
    
    return redirect('gestion:revisar_solicitudes')


@role_required("ADMIN")
@require_http_methods(["POST"])
def rechazar_proyecto(request, pk):
    """
    Rechaza un proyecto y lo marca como rechazado.
    Ahora guarda el motivo de rechazo en la BD.
    """
    proyecto = get_object_or_404(SolicitudProyecto, pk=pk)
    
    # Obtener el motivo de rechazo del formulario
    motivo_rechazo = request.POST.get('motivo_rechazo', '').strip()
    
    # Validar que el motivo no esté vacío
    if not motivo_rechazo:
        messages.error(request, "⚠️ Debes proporcionar un motivo para el rechazo.")
        return redirect('gestion:revisar_solicitudes')
    
    # Actualizar el proyecto
    proyecto.estado = "RECHAZADO"
    proyecto.motivo_rechazo = motivo_rechazo
    proyecto.save()
    
    # Mensaje de advertencia
    messages.warning(
        request, 
        f"❌ Proyecto '{proyecto.nombre}' ha sido rechazado. "
        f"La empresa ha sido notificada del motivo."
    )
    
    return redirect('gestion:revisar_solicitudes')