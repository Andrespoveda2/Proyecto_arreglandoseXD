from django.contrib import admin
from .models import AsignacionInstructor

@admin.register(AsignacionInstructor)
class AsignacionInstructorAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'proyecto', 'fecha_asignacion')
    search_fields = ('instructor__username', 'proyecto__nombre')