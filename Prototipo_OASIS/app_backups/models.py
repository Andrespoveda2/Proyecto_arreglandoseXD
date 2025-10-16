from django.db import models
from django.utils import timezone

class Backup(models.Model):
    nombre = models.CharField(max_length=200)
    ruta = models.FilePathField(path="backups/", match=".*\.sqlite3$", recursive=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    tamano = models.FloatField(help_text="Tamaño en MB")

    def __str__(self):
        return f"{self.nombre} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"

