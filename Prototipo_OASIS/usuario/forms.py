from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, PerfilEmpresa, PerfilInstructor, PerfilAprendiz


# --- Formulario de Registro de Usuario (con rol) ---
class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES, label="Rol del Usuario")

    class Meta:
        model = Usuario
        fields = ["username", "email", "rol", "password1", "password2"]


# --- Formulario de Inicio de Sesión ---
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


# --- Formularios de Perfiles ---

class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = ["nit", "telefono", "sector"]


class PerfilAprendizForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendiz
        fields = ["documento", "ficha", "programa"]


class PerfilInstructorForm(forms.ModelForm):
    class Meta:
        model = PerfilInstructor
        fields = ["documento", "area_conocimiento"]
