from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# --- FUNCIÓN CRÍTICA PARA EL LOGIN_REDIRECT_URL ---
@login_required
def redirect_by_role(request):
    """Redirige a los usuarios basados en su rol después del login."""
    user = request.user
    
    # Asume que el modelo de usuario tiene un campo 'rol' o comprueba si es admin/staff
    if user.is_staff and user.is_superuser:
        return redirect('gestion:dashboard_gestion')
    elif hasattr(user, 'rol'): # Solo para evitar fallos si el campo 'rol' aún no existe en el objeto
        if user.rol == 'Empresa':
            return redirect('empresas:dashboard_empresa')
        elif user.rol == 'Instructor':
            return redirect('instructores:dashboard_instructor')
        elif user.rol == 'Aprendiz':
            return redirect('aprendices:dashboard_aprendiz')
            
    # Redirección de seguridad si el rol no coincide
    return redirect('home:inicio') 

# Placeholder para la vista de registro
def registro_usuario(request):
    return HttpResponse("Página de Registro de Usuario")
