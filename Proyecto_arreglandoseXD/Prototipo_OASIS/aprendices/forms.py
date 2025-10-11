# aprendices/forms.py
from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = []  # No hay campos que el aprendiz llene manualmente
