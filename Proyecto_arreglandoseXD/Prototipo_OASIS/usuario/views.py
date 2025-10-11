from django.contrib.auth import authenticate, login
from django.contrib import messages
from usuario.utils import role_required
from django.shortcuts import render, redirect
from .forms import (
    LoginForm,
    RegistroAprendizForm,
    RegistroEmpresaForm,
    RegistroInstructorForm,
    ProgramaFormativoForm
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
            elif user.rol == Usuario.APRENDIZ:
                return redirect('aprendices:perfil_aprendiz')
            elif user.rol == Usuario.EMPRESA:
                return redirect('empresas:dashboard_empresa')
            elif user.rol == Usuario.INSTRUCTOR:
                return redirect('instructores:dashboard_instructor')
            else:
                return redirect('home:index')  # fallback por defecto
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


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