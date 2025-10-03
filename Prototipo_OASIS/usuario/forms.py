from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, PerfilEmpresa, PerfilInstructor, PerfilAprendiz, ProgramaFormativo

# --- Registro Aprendiz ---
class RegistroAprendizForm(UserCreationForm):
    documento = forms.CharField(label="Documento de Identidad", max_length=10)
    ficha = forms.CharField(label="Ficha de Formación", max_length=20)
    programa = forms.ModelChoiceField(
        queryset=ProgramaFormativo.objects.all(),
        label="Programa de Formación"
    )

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
                programa=self.cleaned_data['programa'],  # Ahora es un objeto ProgramaFormativo
            )
        return user


# --- Registro Empresa ---
class RegistroEmpresaForm(UserCreationForm):
    nit = forms.CharField(label="NIT", max_length=20)
    telefono = forms.CharField(label="Teléfono", max_length=20)
    sector = forms.CharField(label="Sector empresarial", max_length=100)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

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
    documento = forms.CharField(label="Documento de Identidad", max_length=20)
    area_conocimiento = forms.CharField(label="Área de Conocimiento", max_length=100)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

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


# --- Login ---
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


# --- Formularios de Perfiles ---
class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = ["nit", "telefono", "sector"]
        labels = {
            'nit': 'NIT',
            'telefono': 'Teléfono',
            'sector': 'Sector empresarial',
        }


class PerfilAprendizForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendiz
        fields = ["documento", "ficha", "programa"]
        labels = {
            'documento': 'Documento',
            'ficha': 'Ficha de formación',
            'programa': 'Programa de formación',
        }


class PerfilInstructorForm(forms.ModelForm):
    class Meta:
        model = PerfilInstructor
        fields = ["documento", "area_conocimiento"]
        labels = {
            'documento': 'Documento',
            'area_conocimiento': 'Área de conocimiento',
        }
        
class ProgramaFormativoForm(forms.ModelForm):
    class Meta:
        model = ProgramaFormativo
        fields = ['nombre', 'descripcion', 'tipo', 'codigo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
