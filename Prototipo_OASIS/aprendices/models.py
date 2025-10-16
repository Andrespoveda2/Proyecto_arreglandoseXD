# aprendices/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from usuario.models import PerfilAprendiz
from empresas.models import SolicitudProyecto
        
class AprendizProfile(models.Model):
    """
    Modelo para almacenar información extendida del Aprendiz que no está en el modelo User de Django.
    Se usa settings.AUTH_USER_MODEL para referenciar el modelo de usuario definido en el proyecto.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # <--- CAMBIO CLAVE AQUÍ
        on_delete=models.CASCADE, 
        primary_key=True
    )
    
    # Campo para la ficha, simulado como no editable por ahora.
    ficha = models.CharField(
        max_length=10, 
        default='N/A', 
        verbose_name='Número de Ficha'
    ) 
    
    celular = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        verbose_name='Número de Celular'
    )
    
    foto_perfil = models.ImageField(
        upload_to='aprendices/fotos_perfil/', 
        blank=True, 
        null=True, 
        verbose_name='Foto de Perfil'
    )

    class Meta:
        verbose_name = "Perfil de Aprendiz"
        verbose_name_plural = "Perfiles de Aprendices"

    def __str__(self):
        return f"Perfil de {self.user.username}"
