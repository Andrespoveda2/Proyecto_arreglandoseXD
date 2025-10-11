# aprendices/models.py
from django.db import models
from usuario.models import PerfilAprendiz
from empresas.models import SolicitudProyecto

class Postulacion(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("ACEPTADA", "Aceptada"),
        ("RECHAZADA", "Rechazada"),
    ]

    aprendiz = models.ForeignKey(
        PerfilAprendiz,
        on_delete=models.CASCADE,
        related_name="postulaciones"
    )
    proyecto = models.ForeignKey(
        SolicitudProyecto,
        on_delete=models.CASCADE,
        related_name="postulaciones"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="PENDIENTE")
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aprendiz.usuario.username} → {self.proyecto.nombre} ({self.estado})"

    class Meta:
        verbose_name = "Postulación de Aprendiz"
        verbose_name_plural = "Postulaciones de Aprendices"
        unique_together = ("aprendiz", "proyecto")
