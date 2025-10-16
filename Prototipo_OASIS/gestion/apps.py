from django.apps import AppConfig

class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'  # Debe coincidir con el nombre de la carpeta
    verbose_name = 'Gestión Administrativa OASIS'
    label = 'gestion'
