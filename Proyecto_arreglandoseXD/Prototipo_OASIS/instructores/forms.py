from django import forms
from empresas.models import SolicitudProyecto

class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProyecto
        fields = ['descripcion', 'estado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
