from django.db import models
from usuario.models import Usuario
from empresas.models import SolicitudProyecto  # Importamos el modelo de proyecto existente

class AsignacionInstructor(models.Model):
    instructor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'INSTRUCTOR'},
        related_name='asignaciones_instructor'
    )
    proyecto = models.ForeignKey(
        SolicitudProyecto,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    fecha_asignacion = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Asignación de Instructor"
        verbose_name_plural = "Asignaciones de Instructores"
        unique_together = ('instructor', 'proyecto')  # Evita asignaciones duplicadas

    def __str__(self):
        return f"{self.instructor.username} - {self.proyecto.nombre}"
