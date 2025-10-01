from django.apps import AppConfig

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin' # Nombre de la carpeta Python
    verbose_name = 'Gestión Administrativa OASIS'
    label = 'gestion' # <--- para que funcione la URL y que Django sepa que es una app