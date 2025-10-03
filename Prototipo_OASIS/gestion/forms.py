# gestion/forms.py
from django import forms
from usuario.models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'password', 'is_active']
