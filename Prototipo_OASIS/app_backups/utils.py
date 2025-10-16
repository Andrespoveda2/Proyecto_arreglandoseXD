import os
import shutil
from datetime import datetime
from django.conf import settings
from .models import Backup

def crear_backup():
    backup_dir = os.path.join(settings.BASE_DIR, "backups")
    os.makedirs(backup_dir, exist_ok=True)

    db_path = settings.DATABASES['default']['NAME']

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"backup_{fecha}.sqlite3"
    ruta_backup = os.path.join(backup_dir, nombre_archivo)

    shutil.copy2(db_path, ruta_backup)
    tamano_mb = os.path.getsize(ruta_backup) / (1024 * 1024)

    Backup.objects.create(
        nombre=nombre_archivo,
        ruta=ruta_backup,
        tamano=round(tamano_mb, 2)
    )

    return nombre_archivo


def eliminar_backup(backup_id):
    """Elimina el archivo físico y su registro en BD"""
    try:
        backup = Backup.objects.get(id=backup_id)
        if os.path.exists(backup.ruta):
            os.remove(backup.ruta)
        backup.delete()
        return True
    except Backup.DoesNotExist:
        return False


def restaurar_backup(backup_id):
    """Restaura la base de datos a un respaldo anterior"""
    from pathlib import Path
    backup = Backup.objects.get(id=backup_id)
    db_path = settings.DATABASES['default']['NAME']

    # Convertir a string por compatibilidad con Pathlib (Windows/Linux)
    db_path = str(db_path)

    # Hacemos copia de seguridad del estado actual antes de sobrescribir
    copia_seguridad_actual = db_path + ".temp"
    shutil.copy2(db_path, copia_seguridad_actual)

    try:
        # Reemplazar base de datos con el respaldo seleccionado
        shutil.copy2(backup.ruta, db_path)
        return True
    except Exception as e:
        # En caso de error, restauramos la copia temporal
        shutil.copy2(copia_seguridad_actual, db_path)
        print(f"Error al restaurar: {e}")
        return False
    finally:
        # Eliminar copia temporal si existe
        if os.path.exists(copia_seguridad_actual):
            os.remove(copia_seguridad_actual)


