from django import forms
from .models import SolicitudProyecto
from usuario.models import PerfilAprendiz, PerfilInstructor, PerfilEmpresa


class SolicitudProyectoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProyecto
        fields = [
            'nombre',
            'descripcion',
            'area',
            'programa_formativo',
            'duracion_semanas',
            'estado',
            'empresa',
            'aprendices',
            'instructor'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar los campos por perfil correspondiente
        self.fields['empresa'].queryset = PerfilEmpresa.objects.all()
        self.fields['aprendices'].queryset = PerfilAprendiz.objects.all()
        self.fields['instructor'].queryset = PerfilInstructor.objects.all()
