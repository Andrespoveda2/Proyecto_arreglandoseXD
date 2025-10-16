from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from usuario.models import (
    PerfilEmpresa, 
    PerfilAprendiz, 
    PerfilInstructor, 
    ProgramaFormativo,
    SectorProductivo
)
 # Importa el modelo Sector si está en el mismo módulo


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

    AREA_CHOICES = [
        ("DES", "Desarrollo de Software"),
        ("IND", "Ingeniería Industrial"),
        ("ADM", "Administración y Gestión Empresarial"),
        ("ELE", "Electricidad y Electrónica"),
        ("MEC", "Mecánica y Mantenimiento"),
        ("CON", "Construcción e Infraestructura"),
        ("AMB", "Medio Ambiente y Energías Renovables"),
        ("SAL", "Salud y Bienestar"),
        ("TUR", "Turismo y Hotelería"),
        ("ART", "Arte, Diseño y Multimedia"),
    ]

    area = models.CharField(
        max_length=3,
        choices=AREA_CHOICES,
        verbose_name="Área de Aplicación"
    )
    
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
        related_name="solicitudes_asignadas",  # 🔹 cambiado para evitar conflicto
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
        return f"{self.nombre} ({self.get_estado_display()})" #type: ignore

    class Meta:
        verbose_name = "Solicitud de Proyecto"
        verbose_name_plural = "Solicitudes de Proyectos"


class Postulacion(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("ACEPTADA", "Aceptada"),
        ("RECHAZADA", "Rechazada"),
    ]

    aprendiz = models.ForeignKey(
        PerfilAprendiz,
        on_delete=models.CASCADE,
        related_name='postulaciones_proyecto',
        verbose_name="Aprendiz"
    )

    proyecto = models.ForeignKey(
        SolicitudProyecto,
        on_delete=models.CASCADE,
        related_name='postulaciones_aprendices',
        verbose_name="Proyecto"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="PENDIENTE",
        verbose_name="Estado de la Postulación"
    )

    fecha_postulacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Postulación"
    )

    class Meta:
        unique_together = ('aprendiz', 'proyecto')
        verbose_name = "Postulación de Aprendiz"
        verbose_name_plural = "Postulaciones de Aprendices"

    def __str__(self):
        return f"{self.aprendiz.usuario.username} → {self.proyecto.nombre} ({self.estado})"
    
    
class PostulacionInstructor(models.Model):
    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("ACEPTADA", "Aceptada"),
        ("RECHAZADA", "Rechazada"),
    ]

    instructor = models.ForeignKey(
        PerfilInstructor,
        on_delete=models.CASCADE,
        related_name="postulaciones_instructor",
        verbose_name="Instructor"
    )
    proyecto = models.ForeignKey(
        SolicitudProyecto,
        on_delete=models.CASCADE,
        related_name="postulaciones_instructores",
        verbose_name="Proyecto"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="PENDIENTE",
        verbose_name="Estado de la Postulación"
    )
    fecha_postulacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Postulación")

    class Meta:
        unique_together = ('instructor', 'proyecto')
        verbose_name = "Postulación de Instructor"
        verbose_name_plural = "Postulaciones de Instructores"

    def __str__(self):
        return f"{self.instructor.usuario.username} → {self.proyecto.nombre} ({self.estado})"
# Asumimos que el tamaño de la empresa es una selección predefinida
class TamanoEmpresa(models.TextChoices):
    """Opciones predefinidas para el tamaño de la empresa (número de empleados)."""
    # El NameError de '_' se corrige con el import arriba.
    MICRO = 'Micro', _('1 a 10 empleados')
    PEQUENA = 'Pequeña', _('11 a 50 empleados')
    MEDIANA = 'Mediana', _('51 a 250 empleados')
    GRANDE = 'Grande', _('Más de 250 empleados')


class Empresa(models.Model):
    """Modelo para almacenar el perfil corporativo de una empresa."""
    
    # RELACIÓN CON EL USUARIO (Clave foránea al modelo de usuario de Django)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # SOLUCIÓN 2: Cambiamos el related_name a 'perfil_corporativo' 
        # para evitar el conflicto con el modelo 'usuario.PerfilEmpresa'.
        related_name='perfil_corporativo', 
        verbose_name="Usuario de Contacto"
    )

    # INFORMACIÓN BÁSICA Y LEGAL
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    # El campo NIT no se incluye en el formulario de edición, pero está en el modelo.
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT / Identificación Fiscal")
    logo = models.ImageField(
        upload_to='logos_empresas/', # Asegúrate de configurar MEDIA_ROOT en settings.py
        blank=True,
        null=True,
        verbose_name="Logo Corporativo"
    )

    # CLASIFICACIÓN
    sector = models.ForeignKey(
        SectorProductivo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Sector Productivo"
    )
    tamano = models.CharField(
        max_length=10,
        choices=TamanoEmpresa.choices,
        blank=True,
        null=True,
        verbose_name="Tamaño de la Empresa"
    )

    # CONTACTO
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono de Contacto")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección Principal")
    
    # METADATOS
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.razon_social
