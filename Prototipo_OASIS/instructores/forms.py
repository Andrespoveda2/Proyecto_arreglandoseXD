from django import forms
from empresas.models import SolicitudProyecto
from .models import InstructorProfile

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
            'numero_identificacion', 
            'fecha_nacimiento', 
            'bio', 
            'nivel_certificacion', 
            'foto_perfil'
        ]
        widgets = {
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'nivel_certificacion': forms.Select(attrs={'class': 'form-select'}),
            # Foto de perfil no necesita widget especial si es ImageField
        }
        labels = {
            'numero_identificacion': 'No. de Identificación',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'bio': 'Biografía',
            'nivel_certificacion': 'Nivel de Certificación',
            'foto_perfil': 'Foto de Perfil',
        }
