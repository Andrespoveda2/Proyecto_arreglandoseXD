# gestion/forms.py
from django import forms
from usuario.models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        # 🔹 Eliminamos 'is_active' del formulario
        fields = ['username', 'email', 'rol', 'password']

    def save(self, commit=True):
        """
        Guarda el usuario siempre como activo.
        """
        user = super().save(commit=False)
        user.is_active = True  # Se activa automáticamente
        if commit:
            user.save()
        return user
