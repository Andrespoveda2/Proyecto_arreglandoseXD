from django.contrib.auth.models import AbstractUser
from django.db import models

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
    """
    Define los programas de formación (ej: ADSO, Análisis de datos).
    Usado por PerfilAprendiz y SolicitudProyecto.
    """
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Programa de Formación")
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del Programa")
    
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

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    
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
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_aprendiz')
    documento = models.CharField(max_length=20, unique=True, verbose_name="Número de Documento")
    ficha = models.CharField(max_length=10, verbose_name="Número de Ficha")
    programa = models.ForeignKey(ProgramaFormativo, on_delete=models.SET_NULL, null=True, verbose_name="Programa de Formación")
    
    def __str__(self):
        return f"Aprendiz: {self.usuario.username}"

    class Meta:
        verbose_name = "Perfil de Aprendiz"
        verbose_name_plural = "Perfiles de Aprendices"


class PerfilInstructor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_instructor')
    documento = models.CharField(max_length=20, unique=True, verbose_name="Número de Documento")
    area_conocimiento = models.CharField(max_length=100, verbose_name="Área de Conocimiento")
    
    def __str__(self):
        return f"Instructor: {self.usuario.username}"

    class Meta:
        verbose_name = "Perfil de Instructor"
        verbose_name_plural = "Perfiles de Instructores"