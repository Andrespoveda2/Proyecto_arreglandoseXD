from django import forms
from .models import SolicitudProyecto, Empresa, TamanoEmpresa, SectorProductivo
from usuario.models import PerfilAprendiz, PerfilInstructor, PerfilEmpresa, SectorProductivo

class SolicitudProyectoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProyecto
        fields = [
            'nombre',
            'descripcion',
            'area',
            'programa_formativo',
            'duracion_semanas',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'programa_formativo': forms.Select(attrs={'class': 'form-select'}),
            'duracion_semanas': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Quitar cualquier campo no necesario (empresa, estado, aprendices, instructor)
        for campo in ['empresa', 'estado', 'aprendices', 'instructor']:
            if campo in self.fields:
                self.fields.pop(campo)

 

# --- WIDGETS PERSONALIZADOS PARA ESTILOS DE BOOTSTRAP ---
# Estos widgets aplican la clase 'form-control' y esquinas redondeadas 
# a todos los campos de texto, teléfono, etc.
class CustomTextInput(forms.TextInput):
    """Widget para campos de texto con clase form-control de Bootstrap y esquinas redondeadas."""
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control rounded-lg'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class CustomSelect(forms.Select):
    """Widget para campos de selección con clase form-select de Bootstrap."""
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-select rounded-lg'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class CustomClearableFileInput(forms.ClearableFileInput):
    """Widget para campos de subida de archivo (como el logo) con estilos de Bootstrap."""
    def __init__(self, attrs=None):
        # La clase 'form-control' asegura que se vea bien en la plantilla
        default_attrs = {'class': 'form-control rounded-lg form-control-file'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

# --- FORMULARIO PRINCIPAL ---
class EmpresaProfileForm(forms.ModelForm):
    """Formulario para la edición del perfil corporativo de la empresa."""

    class Meta:
        model = Empresa
        # Definición de los campos que el usuario podrá editar en la vista.
        # El campo 'nit' no está aquí ya que generalmente no es editable.
        fields = ['razon_social', 'logo', 'telefono', 'direccion', 'sector', 'tamano']
        
        # Asignación de los widgets personalizados a cada campo
        widgets = {
            'razon_social': CustomTextInput(),
            'telefono': CustomTextInput(attrs={'placeholder': 'Ej: +57 300 123 4567'}),
            'direccion': CustomTextInput(attrs={'placeholder': 'Ej: Calle 10 # 5-20, Ciudad'}),
            'sector': CustomSelect(),
            'tamano': CustomSelect(),
            'logo': CustomClearableFileInput(attrs={'accept': 'image/*'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Lógica de personalización del formulario (ej. etiquetas vacías)

        # 1. Configuración del campo Sector
        if 'sector' in self.fields:
            # Asegura que el queryset cargue todos los sectores disponibles
            self.fields['sector'].queryset = SectorProductivo.objects.all()   # type: ignore
            self.fields['sector'].empty_label = "Seleccione el sector productivo" #type: ignore

        # 2. Configuración del campo Tamaño
        if 'tamano' in self.fields:
            # Personaliza las opciones para que se vean más amigables en el dropdown
            self.fields['tamano'].choices = [(TamanoEmpresa.MICRO, 'Micro (1-10)'),  #type: ignore
                                             (TamanoEmpresa.PEQUENA, 'Pequeña (11-50)'),
                                             (TamanoEmpresa.MEDIANA, 'Mediana (51-250)'),
                                             (TamanoEmpresa.GRANDE, 'Grande (+250)')]
            self.fields['tamano'].empty_label = "Seleccione el rango de empleados" #type: ignore
            
        # 3. Marcar campos obligatorios si el modelo lo requiere (opcional, pero útil para UX)
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['required'] = 'required'
