from django.db import models
from usuario.models import Usuario, ProgramaFormativo # Importamos lo necesario de la app 'usuario'

class SolicitudProyecto(models.Model):
    ESTADO_CHOICES = [
        ("EN_DESARROLLO", "En desarrollo"),
        ("COMPLETADO", "Completado"),
        ("PENDIENTE", "Pendiente/Revisión"),
        ("APROBADO", "Aprobado para Asignación"),
        ("RECHAZADO", "Rechazado"),
    ]
    
    # --- Datos de la Solicitud ---
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Proyecto")
    descripcion = models.TextField(verbose_name="Descripción Detallada")
    area = models.CharField(max_length=100, verbose_name="Área de Aplicación")
    
    # Nuevo campo para el programa que busca el proyecto
    programa_formativo = models.ForeignKey(
        ProgramaFormativo, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Programa Formativo Requerido"
    )
    
    duracion_semanas = models.PositiveIntegerField(verbose_name="Duración Estimada (Semanas)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE", verbose_name="Estado del Proyecto")
    
    # --- Relaciones ---
    # La empresa que crea el proyecto
    empresa = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': Usuario.EMPRESA}, # Solo permite seleccionar usuarios con rol EMPRESA
        related_name="proyectos_empresa", 
        verbose_name="Empresa Solicitante"
    )
    
    # Aprendices asignados (puede ser un grupo o un solo aprendiz)
    aprendices = models.ManyToManyField(
        Usuario, 
        blank=True, 
        limit_choices_to={'rol': Usuario.APRENDIZ}, # Solo permite seleccionar aprendices
        related_name="proyectos_asignados", 
        verbose_name="Aprendices Asignados"
    )
    
    # Instructor supervisor (opcional)
    instructor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'rol': Usuario.INSTRUCTOR}, # Solo permite seleccionar instructores
        related_name="proyectos_supervisados",
        verbose_name="Instructor Supervisor"
    )
    
    # --- Metadatos ---
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"
    
    class Meta:
        verbose_name = "Solicitud de Proyecto"
        verbose_name_plural = "Solicitudes de Proyectos"
