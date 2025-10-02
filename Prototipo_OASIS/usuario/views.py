from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import (
    LoginForm,
    RegistroAprendizForm,
    RegistroEmpresaForm,
    RegistroInstructorForm
)
from .models import Usuario


# -------- Login General --------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirección personalizada según rol
            if user.is_superuser or (user.rol == Usuario.ADMIN and user.is_staff):
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
            return redirect('login')  # o una vista de éxito
    else:
        form = RegistroAprendizForm()
    return render(request, 'registro_aprendiz.html', {'form': form})


def registro_empresa(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroEmpresaForm()
    return render(request, 'registro_empresa.html', {'form': form})


def registro_instructor(request):
    if request.method == 'POST':
        form = RegistroInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroInstructorForm()
    return render(request, 'registro_instructor.html', {'form': form})
