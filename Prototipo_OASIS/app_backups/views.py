from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Backup
from .utils import crear_backup, eliminar_backup, restaurar_backup
from django.contrib.admin.views.decorators import staff_member_required


def lista_backups(request):
    backups = Backup.objects.all().order_by('-fecha_creacion')
    return render(request, "app_backups/backup_list.html", {"backups": backups})

@staff_member_required
def crear_backup_view(request):
    if request.method == "POST":
        nombre = crear_backup()
        messages.success(request, f"Respaldo '{nombre}' creado exitosamente.")
    return redirect("lista_backups")

@staff_member_required
def eliminar_backup_view(request, backup_id):
    if eliminar_backup(backup_id):
        messages.success(request, "Respaldo eliminado correctamente.")
    else:
        messages.error(request, "No se pudo eliminar el respaldo.")
    return redirect("lista_backups")

def restaurar_backup_view(request, backup_id):
    if restaurar_backup(backup_id):
        messages.success(request, "✅ Base de datos restaurada correctamente.")
    else:
        messages.error(request, "❌ Error al restaurar el respaldo.")
    return redirect("lista_backups")

