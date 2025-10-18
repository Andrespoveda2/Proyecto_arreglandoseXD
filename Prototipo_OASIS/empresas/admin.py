from django.contrib import admin
from .models import SolicitudProyecto

class SolicitudProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'creado_en', 'fecha_decision')
    list_filter = ('estado', 'creado_en')
    search_fields = ('nombre', 'empresa__usuario__username')
    readonly_fields = ('motivo_aprobacion', 'motivo_rechazo', 'fecha_decision', 'creado_en')
    
    fieldsets = (
        ('Información del Proyecto', {
            'fields': ('nombre', 'empresa', 'descripcion', 'area', 'creado_en')
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_decision')
        }),
        ('Retroalimentación', {
            'fields': ('motivo_aprobacion', 'motivo_rechazo')
        }),
    )

admin.site.register(SolicitudProyecto, SolicitudProyectoAdmin)