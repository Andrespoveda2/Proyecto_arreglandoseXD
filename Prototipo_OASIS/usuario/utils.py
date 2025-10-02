from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login

def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user

            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            # ✅ Superusuario siempre entra
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            if hasattr(user, 'rol') and user.rol in allowed_roles:
                return view_func(request, *args, **kwargs)

            return redirect_to_login(request.get_full_path())

        return _wrapped_view
    return decorator

