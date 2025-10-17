from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# --- MODELOS AUXILIARES (Necesarios para Perfiles) ---

class SectorProductivo(models.Model):
    """
    Define los sectores productivos (ej: Tecnología, Construcción, Salud).
    Usado por PerfilEmpresa.
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Sector Productivo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Sector")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Sector Productivo"
        verbose_name_plural = "Sectores Productivos"


class ProgramaFormativo(models.Model):
    TECNICO = "TECNICO"
    TECNOLOGO = "TECNOLOGO"
    ESPECIALIZACION = "ESPECIALIZACION"
    UNIVERSITARIO = "UNIVERSITARIO"

    TIPOS = [
        (TECNICO, "Técnico"),
        (TECNOLOGO, "Tecnólogo"),
        (ESPECIALIZACION, "Especialización Tecnológica"),
        (UNIVERSITARIO, "Universitario"),
    ]

    nombre = models.CharField(max_length=150, unique=True, verbose_name="Programa de Formación")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name="Tipo de Programa")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del Programa")
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Programa Formativo"
        verbose_name_plural = "Programas Formativos"


# --- MODELO BASE DE USUARIO (El que extiende AbstractUser) ---

class Usuario(AbstractUser):
    ADMIN = "ADMIN"
    EMPRESA = "EMPRESA"
    APRENDIZ = "APRENDIZ"
    INSTRUCTOR = "INSTRUCTOR"

    ROLES = [
        (ADMIN, "Administrador"),
        (EMPRESA, "Empresa"),
        (APRENDIZ, "Aprendiz"),
        (INSTRUCTOR, "Instructor"),
    ]

    # Tomamos el campo 'rol' del código de tu compañero, es el que define la lógica.
    rol = models.CharField(max_length=20, choices=ROLES, default=APRENDIZ, verbose_name="Rol del Usuario")
    
    # Campo extra si queremos deshabilitar al usuario sin borrarlo
    esta_activo = models.BooleanField(default=True, verbose_name="Está Activo")
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = self.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"


# --- MODELOS DE PERFILES (Datos Únicos) ---
# Usamos OneToOneField para ligar los datos únicos a la instancia de Usuario.

class PerfilEmpresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_empresa')
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    sector = models.ForeignKey(SectorProductivo, on_delete=models.SET_NULL, null=True, verbose_name="Sector Productivo")

    def __str__(self):
        return f"Empresa: {self.razon_social}"

    class Meta:
        verbose_name = "Perfil de Empresa"
        verbose_name_plural = "Perfiles de Empresas"


class PerfilAprendiz(models.Model):
    TIPOS_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('TI', 'Tarjeta de Identidad'),
        ('DNI', 'DNI'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_aprendiz')
    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPOS_DOCUMENTO,
        default='CC',
        verbose_name="Tipo de Documento",
        help_text="Selecciona tu tipo de documento"
    )
    documento = models.CharField(max_length=20, unique=True, verbose_name="Número de Documento")
    ficha = models.CharField(max_length=10, verbose_name="Número de Ficha")
    programa = models.ForeignKey(ProgramaFormativo, on_delete=models.SET_NULL, null=True, verbose_name="Programa de Formación")
    
    def __str__(self):
        return f"Aprendiz: {self.usuario.username}"

    class Meta:
        verbose_name = "Perfil de Aprendiz"
        verbose_name_plural = "Perfiles de Aprendices"


class PerfilInstructor(models.Model):
    TIPOS_DOCUMENTO = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('TI', 'Tarjeta de Identidad'),
        ('DNI', 'DNI'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_instructor')
    tipo_documento = models.CharField(
        max_length=10,
        choices=TIPOS_DOCUMENTO,
        default='CC',
        verbose_name="Tipo de Documento",
        help_text="Selecciona tu tipo de documento"
    )
    documento = models.CharField(max_length=20, unique=True, verbose_name="Número de Documento")
    area_conocimiento = models.CharField(max_length=100, verbose_name="Área de Conocimiento")
    
    def __str__(self):
        return f"Instructor: {self.usuario.username}"

    class Meta:
        verbose_name = "Perfil de Instructor"
        verbose_name_plural = "Perfiles de Instructores"


class MensajeContacto(models.Model):
    """
    Modelo para almacenar los mensajes enviados a través del formulario
    de Contacto/Soporte.
    """
    
    # Opciones para el campo de asunto (deben coincidir con el template contacto.html)
    ASUNTO_CHOICES = (
        ('soporte_tecnico', 'Soporte Técnico (Error, Bug)'),
        ('consulta_general', 'Consulta General sobre el Proyecto'),
        ('sugerencia', 'Sugerencia o Colaboración'),
        ('otro', 'Otro Motivo'),
    )
    
    # Campo para identificar al usuario logueado (si lo hay)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario Asociado'
    )
    
    # Información obligatoria del formulario
    nombre = models.CharField(max_length=100, verbose_name='Nombre de Contacto')
    email = models.EmailField(max_length=150, verbose_name='Correo Electrónico')
    asunto = models.CharField(max_length=50, choices=ASUNTO_CHOICES, verbose_name='Asunto de la Consulta')
    mensaje = models.TextField(verbose_name='Mensaje Detallado')
    
    # Metadatos
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Envío')
    resuelto = models.BooleanField(default=False, verbose_name='Resuelto')
    
    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']

    def __str__(self):
        asunto_display = dict(self.ASUNTO_CHOICES).get(self.asunto, self.asunto)
        return f"[{asunto_display}] de {self.nombre} ({self.fecha_envio.strftime('%Y-%m-%d')})"