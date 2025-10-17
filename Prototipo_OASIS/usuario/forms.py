from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from .models import Usuario, PerfilEmpresa, PerfilInstructor, PerfilAprendiz, ProgramaFormativo, SectorProductivo, MensajeContacto

# --- Registro Aprendiz ---
class RegistroAprendizForm(UserCreationForm):
    tipo_documento = forms.ChoiceField(
        choices=PerfilAprendiz.TIPOS_DOCUMENTO,
        label="Tipo de Documento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    documento = forms.CharField(
        label="Número de Documento",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1095123456'
        })
    )
    ficha = forms.CharField(
        label="Ficha de Formación",
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    programa = forms.ModelChoiceField(
        queryset=ProgramaFormativo.objects.filter(activo=True),
        label="Programa de Formación",
        empty_label="Selecciona tu programa de formación",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Si no ves tu programa, contacta a un administrador."
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        tipo_documento = self.cleaned_data.get('tipo_documento')
        
        # Validar que el documento no contenga caracteres especiales
        if not documento.isalnum():
            raise forms.ValidationError("El documento solo puede contener números y letras.")
        
        # Validar que el documento no esté registrado
        if PerfilAprendiz.objects.filter(documento=documento).exists():
            raise forms.ValidationError("Este documento ya se encuentra registrado.")
        
        return documento

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.APRENDIZ
        if commit:
            user.save()
            PerfilAprendiz.objects.create(
                usuario=user,
                tipo_documento=self.cleaned_data['tipo_documento'],
                documento=self.cleaned_data['documento'],
                ficha=self.cleaned_data['ficha'],
                programa=self.cleaned_data['programa'], 
            )
        return user


# --- Registro Empresa ---
class RegistroEmpresaForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PerfilEmpresa
        fields = ['razon_social', 'nit', 'telefono', 'sector']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        if PerfilEmpresa.objects.filter(nit=nit).exists():
            raise forms.ValidationError("Este NIT ya se encuentra registrado.")
        return nit

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            cleaned_data = {}
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
    tipo_documento = forms.ChoiceField(
        choices=PerfilInstructor.TIPOS_DOCUMENTO,
        label="Tipo de Documento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    documento = forms.CharField(
        label="Número de Documento",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1095123456'
        })
    )
    area_conocimiento = forms.CharField(
        label="Área de Conocimiento",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Programación, Electrónica, etc.'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        tipo_documento = self.cleaned_data.get('tipo_documento')
        
        # Validar que el documento no contenga caracteres especiales
        if not documento.isalnum():
            raise forms.ValidationError("El documento solo puede contener números y letras.")
        
        # Validar que el documento no esté registrado
        if PerfilInstructor.objects.filter(documento=documento).exists():
            raise forms.ValidationError("Este documento ya se encuentra registrado.")
        
        return documento

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.INSTRUCTOR
        if commit:
            user.save()
            PerfilInstructor.objects.create(
                usuario=user,
                tipo_documento=self.cleaned_data['tipo_documento'],
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
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-control'}),
        }


class PerfilAprendizForm(forms.ModelForm):
    class Meta:
        model = PerfilAprendiz
        fields = ["tipo_documento", "documento", "ficha", "programa"]
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'documento': 'Número de Documento',
            'ficha': 'Ficha de formación',
            'programa': 'Programa de formación',
        }
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'ficha': forms.TextInput(attrs={'class': 'form-control'}),
            'programa': forms.Select(attrs={'class': 'form-control'}),
        }


class PerfilInstructorForm(forms.ModelForm):
    class Meta:
        model = PerfilInstructor
        fields = ["tipo_documento", "documento", "area_conocimiento"]
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'documento': 'Número de Documento',
            'area_conocimiento': 'Área de conocimiento',
        }
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'area_conocimiento': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
class ProgramaFormativoForm(forms.ModelForm):
    class Meta:
        model = ProgramaFormativo
        fields = ['nombre', 'descripcion', 'tipo', 'codigo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SectorProductivoForm(forms.ModelForm):
    class Meta:
        model = SectorProductivo
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

        
class ContactoForm(forms.ModelForm):
    """
    Formulario basado en el modelo MensajeContacto para capturar
    las solicitudes de soporte de los usuarios.
    """
    asunto = forms.ChoiceField(
        choices=[('', 'Selecciona el tema')] + list(MensajeContacto.ASUNTO_CHOICES),
        label='Asunto',
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'})
    )

    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Daniel Gómez',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: tu.correo@sena.edu.co',
                'required': 'required'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Describe tu consulta o problema...',
                'rows': 4,
                'required': 'required'
            }),
        }
        
        labels = {
            'nombre': 'Tu Nombre',
            'email': 'Correo Electrónico',
            'mensaje': 'Mensaje Detallado',
        }


# --- FORMULARIO PARA MOSTRAR CONTRASEÑA EN EL RESETEO ---
class RestablecerContrasenaForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        }), 
        strip=False,
        help_text=("Ingresa una contraseña segura (mínimo 8 caracteres).")
    )
    
    new_password2 = forms.CharField(
        label=_("Confirmación de contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'autocomplete': 'new-password'
        }),
    )