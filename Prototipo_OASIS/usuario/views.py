from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import Usuario

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirige según rol
            if user.rol == Usuario.APRENDIZ:
                return redirect('perfil_aprendiz')
            elif user.rol == Usuario.EMPRESA:
                return redirect('perfil_empresa')
            elif user.rol == Usuario.INSTRUCTOR:
                return redirect('perfil_instructor')
            else:
                return redirect('home')  # o admin dashboard

    else:
        form = LoginForm()
    
    return render(request, 'usuario/login.html', {'form': form})
