from django.shortcuts import render, redirect, get_object_or_404
from usuario.utils import role_required
# Asume que estos modelos y formularios están definidos en la app 'usuario' o en el directorio superior.
from usuario.models import Usuario, ProgramaFormativo, SectorProductivo
from usuario.forms import ProgramaFormativoForm, SectorProductivoForm
from .forms import UsuarioForm # Asume que UsuarioForm está en el mismo directorio de 'gestion'
from django.core.paginator import Paginator
from django.db.models import Count # Se añade para posible uso en reportes, aunque no es estrictamente necesario aquí.

# --- Vistas del Dashboard y Métricas ---

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
