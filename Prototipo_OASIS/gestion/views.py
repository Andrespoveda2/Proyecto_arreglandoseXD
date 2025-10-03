from django.shortcuts import render, redirect, get_object_or_404
from usuario.utils import role_required
from usuario.models import Usuario, ProgramaFormativo
from usuario.forms import ProgramaFormativoForm
from .forms import UsuarioForm
from django.core.paginator import Paginator

# --- Gestión (Admin) ---
@role_required("ADMIN")
def dashboard_admin(request):
    return render(request, 'gestion/dashboard_admin.html', {
        'usuario': request.user,  # 👈 Este es el usuario actual
    })
    

@role_required("ADMIN")
def dashboard_admin(request):
    """Dashboard exclusivo para administradores."""
    total_usuarios = Usuario.objects.count()

    usuarios_por_rol = {
        'admins': Usuario.objects.filter(rol=Usuario.ADMIN).count(),
        'instructores': Usuario.objects.filter(rol=Usuario.INSTRUCTOR).count(),
        'empresas': Usuario.objects.filter(rol=Usuario.EMPRESA).count(),
        'aprendices': Usuario.objects.filter(rol=Usuario.APRENDIZ).count(),
    }

    usuarios_recientes = Usuario.objects.order_by('-date_joined')[:5]

    context = {
        'total_usuarios': total_usuarios,
        'usuarios_por_rol': usuarios_por_rol,
        'usuarios_recientes': usuarios_recientes,
    }
    return render(request, 'dashboard_admin.html')


@role_required("ADMIN")
def listar_usuarios(request):
    """Vista para listar y gestionar usuarios del sistema."""
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


def gestion_programas(request):
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
    }

    return render(request, 'reportes.html', context)


@role_required("ADMIN")
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('gestion:listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

@role_required("ADMIN")
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('gestion:listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
        form.fields['password'].required = False  # para que no sea obligatorio
    return render(request, 'editar_usuario.html', {'form': form})

@role_required("ADMIN")
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('gestion:listar_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})
