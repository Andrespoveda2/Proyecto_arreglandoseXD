from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, PerfilEmpresa, PerfilInstructor, PerfilAprendiz, ProgramaFormativo, SectorProductivo

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
class RegistroEmpresaForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de Usuario")
    email = forms.EmailField(label="Correo Electrónico")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = PerfilEmpresa
        fields = ['razon_social', 'nit', 'telefono', 'sector']
        widgets = {
            'sector': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        usuario = Usuario.objects.create_user(
        username=self.cleaned_data['username'],
        email=self.cleaned_data['email'],
        password=self.cleaned_data['password1'],
        rol=Usuario.EMPRESA
        )
        perfil_empresa = super().save(commit=False)
        perfil_empresa.usuario = usuario
        if commit:
            perfil_empresa.save()
        return usuario

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

class SectorProductivoForm(forms.ModelForm):
    class Meta:
        model = SectorProductivo
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }