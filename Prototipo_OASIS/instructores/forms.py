from django import forms
from empresas.models import SolicitudProyecto
from .models import InstructorProfile
from django.core.exceptions import ValidationError


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProyecto
        fields = ['descripcion', 'estado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = [
            'tipo_documento',
            'numero_identificacion',
            'fecha_nacimiento',
            'bio',
            'nivel_certificacion',
            'foto_perfil'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select form-control-sena', 'id': 'id_tipo_documento'}),
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control form-control-sena', 'id': 'id_numero_identificacion'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control form-control-sena', 'type': 'date', 'id': 'id_fecha_nacimiento'}),
            'bio': forms.Textarea(attrs={'class': 'form-control form-control-sena', 'rows': 4, 'id': 'id_bio'}),
            'nivel_certificacion': forms.Select(attrs={'class': 'form-select form-control-sena', 'id': 'id_nivel_certificacion'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control', 'id': 'id_foto_perfil'}),
        }
        labels = {
            'tipo_documento': 'Tipo de Documento',
            'numero_identificacion': 'Número de Identificación',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'bio': 'Biografía',
            'nivel_certificacion': 'Nivel de Certificación',
            'foto_perfil': 'Foto de Perfil',
        }

    def clean_numero_identificacion(self):
        """Valida que el número de identificación solo tenga dígitos."""
        numero_identificacion = self.cleaned_data.get('numero_identificacion')
        if numero_identificacion and not numero_identificacion.isdigit():
            raise ValidationError("El número de identificación debe contener solo dígitos.")
        return numero_identificacion
