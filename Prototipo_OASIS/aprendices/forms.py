# aprendices/forms.py
from django import forms
from .models import  AprendizProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from empresas.models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = []  # No hay campos que el aprendiz llene manualmente


class UserEditForm(forms.ModelForm):
    """
    Formulario para editar los campos directamente en el modelo User.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        
        # Mapeo a las clases CSS del template (form-control-sena)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sena', 'id': 'id_first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sena', 'id': 'id_last_name'}),
        }

class AprendizProfileForm(forms.ModelForm):
    """
    Formulario para editar los campos del modelo AprendizProfile.
    """
    class Meta:
        model = AprendizProfile
        fields = ('celular', 'foto_perfil')
        
        # Mapeo a las clases CSS del template (form-control-sena)
        widgets = {
            'celular': forms.TextInput(attrs={'class': 'form-control form-control-sena', 'id': 'id_celular'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_foto_perfil'}),
        }
        
    def clean_celular(self):
        """Validación simple para el campo celular."""
        celular = self.cleaned_data.get('celular')
        if celular and not celular.isdigit():
            raise ValidationError("El número de celular debe contener solo dígitos.")
        return celular
