from django.db import models
from usuario.models import Usuario
from empresas.models import SolicitudProyecto
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os


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
        unique_together = ('instructor', 'proyecto')

    def __str__(self):
        return f"{self.instructor.username} - {self.proyecto.nombre}"


def instructor_profile_path(instance, filename):
    return f'instructores/perfil_{instance.usuario.id}/{filename}'


# Opciones para la Certificación del Instructor
class NivelCertificacion(models.TextChoices):
    BASICO = 'Basico', _('Certificación Nivel Básico')
    INTERMEDIO = 'Intermedio', _('Certificación Nivel Intermedio')
    AVANZADO = 'Avanzado', _('Certificación Nivel Avanzado')
    EXPERTO = 'Experto', _('Instructor Experto/Senior')


class InstructorProfile(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_instructor_yl',
        verbose_name='Usuario Asociado'
    )

    # 🔹 Agregamos el campo que faltaba:
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PP', 'Pasaporte'),
        ('OTRO', 'Otro Documento'),
    ]
    
    tipo_documento = models.CharField(
        max_length=5,
        choices=TIPO_DOCUMENTO_CHOICES,
        default='CC',
        verbose_name='Tipo de Documento',
        null=True, 
        blank=True
    )

    numero_identificacion = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='No. de Identificación (Cédula/DNI)',
        null=True, 
        blank=True
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Nacimiento'
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biografía (Máx. 500 caracteres)'
    )

    nivel_certificacion = models.CharField(
        max_length=50,
        choices=NivelCertificacion.choices,
        default=NivelCertificacion.BASICO,
        verbose_name='Nivel de Certificación'
    )

    foto_perfil = models.ImageField(
        upload_to=instructor_profile_path,
        null=True,
        blank=True,
        verbose_name='Foto de Perfil'
    )

    def __str__(self):
        return f"Perfil de Instructor: {self.usuario.get_full_name() or self.usuario.username}"

    class Meta:
        verbose_name = 'Perfil de Instructor'
        verbose_name_plural = 'Perfiles de Instructores'
