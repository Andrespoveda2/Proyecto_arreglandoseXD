from django.db import models
from usuario.models import Usuario
from empresas.models import SolicitudProyecto  # Importamos el modelo de proyecto existente
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
        unique_together = ('instructor', 'proyecto')  # Evita asignaciones duplicadas

    def __str__(self):
        return f"{self.instructor.username} - {self.proyecto.nombre}"


def instructor_profile_path(instance, filename):
    # Archivos subidos a MEDIA_ROOT/instructores/perfil_[ID]/nombre_archivo
    return f'instructores/perfil_{instance.usuario.id}/{filename}'

# Opciones para la Certificación del Instructor
class NivelCertificacion(models.TextChoices):
    BASICO = 'Basico', _('Certificación Nivel Básico')
    INTERMEDIO = 'Intermedio', _('Certificación Nivel Intermedio')
    AVANZADO = 'Avanzado', _('Certificación Nivel Avanzado')
    EXPERTO = 'Experto', _('Instructor Experto/Senior')

class InstructorProfile(models.Model):
    # Relación uno a uno con el usuario. 
    # Usamos related_name para evitar el conflicto que tuvimos con la Empresa.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_instructor_yl', # Nombre único para la relación inversa
        verbose_name='Usuario Asociado'
    )
    
    # Datos personales
    numero_identificacion = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name='No. de Identificación (Cédula/DNI)'
    )
    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Fecha de Nacimiento'
    )

    # Información profesional y biografía
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
    
    # Archivos
    foto_perfil = models.ImageField(
        upload_to=instructor_profile_path,
        null=True, 
        blank=True, 
        verbose_name='Foto de Perfil'
    )
    
    # Métodos
    def __str__(self):
        return f"Perfil de Instructor: {self.usuario.get_full_name() or self.usuario.username}"

    class Meta:
        verbose_name = 'Perfil de Instructor'
        verbose_name_plural = 'Perfiles de Instructores'
        
