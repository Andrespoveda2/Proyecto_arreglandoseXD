from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, PerfilEmpresa, PerfilInstructor, PerfilAprendiz


# --- Formulario de Registro de Usuario (con rol) ---
class RegistroForm(UserCreationForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES, label="Rol del Usuario")

    class Meta:
        model = Usuario
        fields = ["username", "email", "rol", "password1", "password2"]
        
        
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, PerfilAprendiz, PerfilEmpresa, PerfilInstructor


# --- Registro Aprendiz ---
class RegistroAprendizForm(UserCreationForm):
    documento = forms.CharField()
    ficha = forms.CharField()
    programa = forms.CharField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.APRENDIZ
        if commit:
            user.save()
            PerfilAprendiz.objects.create(
                usuario=user,
                documento=self.cleaned_data['documento'],
                ficha=self.cleaned_data['ficha'],
                programa=self.cleaned_data['programa'],
            )
        return user


# --- Registro Empresa ---
class RegistroEmpresaForm(UserCreationForm):
    nit = forms.CharField()
    telefono = forms.CharField()
    sector = forms.CharField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.EMPRESA
        if commit:
            user.save()
            PerfilEmpresa.objects.create(
                usuario=user,
                nit=self.cleaned_data['nit'],
                telefono=self.cleaned_data['telefono'],
                sector=self.cleaned_data['sector'],
            )
        return user


# --- Registro Instructor ---
class RegistroInstructorForm(UserCreationForm):
    documento = forms.CharField()
    area_conocimiento = forms.CharField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.INSTRUCTOR
        if commit:
            user.save()
            PerfilInstructor.objects.create(
                usuario=user,
                documento=self.cleaned_data['documento'],
                area_conocimiento=self.cleaned_data['area_conocimiento'],
            )
        return user



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
