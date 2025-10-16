from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuario.utils import role_required
from django.shortcuts import render, redirect
from .forms import (
    LoginForm,
    RegistroAprendizForm,
    RegistroEmpresaForm,
    RegistroInstructorForm,
    ProgramaFormativoForm,
    ContactoForm
)
from .models import Usuario, ProgramaFormativo


# -------- Login General --------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirección personalizada según rol
            if user.is_superuser or (user.rol == Usuario.ADMIN and user.is_staff): #type: ignore
                return redirect('gestion:dashboard_admin')  # Nombre de tu URL en la app 'gestion'
            elif user.rol == Usuario.APRENDIZ:  #type: ignore
                return redirect('aprendices:dashboard_aprendiz')
            elif user.rol == Usuario.EMPRESA:   #type: ignore
                return redirect('empresas:dashboard_empresa')
            elif user.rol == Usuario.INSTRUCTOR:    #type: ignore
                return redirect('instructores:dashboard_instructor')
            else:
                return redirect('home:index')  # fallback por defecto
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Cierra la sesión del usuario, muestra un mensaje de éxito, y redirige al inicio."""
    
    # Se añade el mensaje ANTES de llamar a logout.
    # El if request.user.is_authenticated: no es estrictamente necesario antes de logout(request),
    # pero es bueno para el mensaje.
    if request.user.is_authenticated:
        messages.info(request, "Sesión cerrada con éxito. ¡Vuelve pronto!")
    
    # Llama a la función de logout de Django para terminar la sesión
    logout(request)
    
    # Redirige a la URL de logout que a su vez redirige a la página de inicio.
    # Esto asegura que se use la vista LogoutView de Django y se muestre cualquier
    # mensaje o plantilla de 'sesión cerrada' si la configuras en el futuro.
    return redirect('auth:logout')

# -------- Página intermedia para elegir tipo de registro --------
def elegir_registro(request):
    return render(request, 'elegir_registro.html')


# -------- Registro para cada rol --------
def registro_aprendiz(request):
    if request.method == 'POST':
        form = RegistroAprendizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aprendiz registrado correctamente. Ahora puedes iniciar sesión.")
            return redirect('auth:login')
    else:
        form = RegistroAprendizForm()
    return render(request, 'registro_aprendiz.html', {'form': form})


def registro_empresa(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La empresa se registró correctamente. Ahora puedes iniciar sesión.")
            return redirect('auth:login')
    else:
        form = RegistroEmpresaForm()
    return render(request, 'registro_empresa.html', {'form': form})


def registro_instructor(request):
    if request.method == 'POST':
        form = RegistroInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor registrado correctamente. Ahora puedes iniciar sesión.")
            return redirect('auth:login')
    else:
        form = RegistroInstructorForm()
    return render(request, 'registro_instructor.html', {'form': form})


@role_required("ADMIN")  # o quien sea que pueda gestionar programas
def gestion_programas(request):
    if request.method == "POST":
        form = ProgramaFormativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Programa formativo creado correctamente.")
            return redirect('gestion:gestion_programas')  # asegúrate de tener el namespace bien configurado
    else:
        form = ProgramaFormativoForm()

    programas = ProgramaFormativo.objects.all().order_by('nombre')

    return render(request, 'gestion_programas.html', {
        'form': form,
        'programas': programas,
    })
    
def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            mensaje_contacto = form.save(commit=False)
            
            # Si el usuario está autenticado, asociamos el mensaje a su perfil
            if request.user.is_authenticated:
                mensaje_contacto.usuario = request.user
            
            mensaje_contacto.save()
            
            # Puedes configurar aquí el envío de un correo electrónico de notificación (opcional)
            
            messages.success(request, "Tu solicitud de soporte ha sido enviada con éxito. ¡Te contactaremos pronto!")
            return redirect('auth:contacto') # Redirige al mismo formulario para evitar reenvío
            
    else:
        # Si el usuario está logueado, pre-llenamos los campos nombre y email
        initial_data = {}
        if request.user.is_authenticated:
            # Asume que tu modelo Usuario tiene campos 'first_name' y 'email'
            initial_data['nombre'] = f"{request.user.first_name} {request.user.last_name}".strip()
            initial_data['email'] = request.user.email
            
        form = ContactoForm(initial=initial_data)

    # Nota: Asume que el nombre de la URL para esta vista es 'home:contacto'
    return render(request, 'contacto.html', {'form': form})


@role_required("ADMIN")
def detalle_usuario_admin(request, pk):
    """
    Vista para que el administrador vea el perfil detallado de cualquier usuario.
    Obtiene el usuario por su PK y luego busca su perfil específico según el rol.
    """
    # 1. Obtener el objeto Usuario principal
    usuario_seleccionado = get_object_or_404(Usuario, pk=pk)
    perfil = None

    # 2. Determinar el rol y obtener el perfil correspondiente
    try:
        if usuario_seleccionado.rol == Usuario.APRENDIZ:
            perfil = usuario_seleccionado.perfil_aprendiz
        elif usuario_seleccionado.rol == Usuario.INSTRUCTOR:
            perfil = usuario_seleccionado.perfil_instructor
        elif usuario_seleccionado.rol == Usuario.EMPRESA:
            perfil = usuario_seleccionado.perfil_empresa
        # Para el rol ADMIN, el perfil puede ser None, lo cual es correcto.
    except (
        Usuario.perfil_aprendiz.RelatedObjectDoesNotExist,
        Usuario.perfil_instructor.RelatedObjectDoesNotExist,
        Usuario.perfil_empresa.RelatedObjectDoesNotExist
    ):
        # Si por alguna razón el perfil no se creó, 'perfil' seguirá siendo None.
        # La plantilla deberá manejar este caso.
        pass
    
    return render(request, 'detalle_usuario.html', {
        'usuario_seleccionado': usuario_seleccionado,
        'perfil': perfil
    })
    
    
def manual_usuario(request):
    """
    Vista para mostrar el manual de usuario.
    """
    return render(request, 'manual_usuario.html')
