from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            # 1. Si el usuario no está autenticado, lo enviamos a la página de login.
            if not user.is_authenticated:
                return redirect(reverse('auth:login') + f'?next={request.get_full_path()}')

            # 2. Si es superusuario, tiene acceso a todo.
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # 3. Si tiene el rol requerido, le damos acceso.
            if hasattr(user, 'rol') and user.rol in allowed_roles:
                return view_func(request, *args, **kwargs)

            # 4. Si está autenticado pero NO tiene el rol, lo redirigimos al inicio con un mensaje.
            # Esto es mucho más claro para el usuario que volver a enviarlo al login.
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('home:inicio') # Redirige a la página de inicio de la app 'home'

        return _wrapped_view
    return decorator
