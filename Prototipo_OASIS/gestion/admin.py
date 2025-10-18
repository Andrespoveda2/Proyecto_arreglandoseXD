from django.contrib import admin

# Register your models here.
class SolicitudProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'creado_en', 'motivo_aprobacion', 'motivo_rechazo')
    readonly_fields = ('motivo_aprobacion', 'motivo_rechazo', 'fecha_decision')