from django.db import models
from usuario.models import (
    PerfilEmpresa, 
    PerfilAprendiz, 
    PerfilInstructor, 
    ProgramaFormativo
)

class SolicitudProyecto(models.Model):
    ESTADO_CHOICES = [
        ("EN_DESARROLLO", "En desarrollo"),
        ("COMPLETADO", "Completado"),
        ("PENDIENTE", "Pendiente/Revisión"),
        ("APROBADO", "Aprobado para Asignación"),
        ("RECHAZADO", "Rechazado"),
    ]

    # --- Datos del Proyecto ---
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Proyecto")
    descripcion = models.TextField(verbose_name="Descripción Detallada")
    area = models.CharField(max_length=100, verbose_name="Área de Aplicación")
    duracion_semanas = models.PositiveIntegerField(verbose_name="Duración Estimada (Semanas)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PENDIENTE", verbose_name="Estado del Proyecto")
    
    # --- Relaciones ---
    empresa = models.ForeignKey(
        PerfilEmpresa,
        on_delete=models.CASCADE,
        related_name="proyectos",
        verbose_name="Empresa Solicitante"
    )

    aprendices = models.ManyToManyField(
        PerfilAprendiz,
        blank=True,
        related_name="proyectos_asignados",
        verbose_name="Aprendices Asignados"
    )

    instructor = models.ForeignKey(
        PerfilInstructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proyectos_supervisados",
        verbose_name="Instructor Supervisor"
    )

    programa_formativo = models.ForeignKey(
        ProgramaFormativo,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Programa Formativo Requerido"
    )

    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Solicitud de Proyecto"
        verbose_name_plural = "Solicitudes de Proyectos"

