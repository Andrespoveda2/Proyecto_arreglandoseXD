from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='usuario.Usuario')
def crear_perfil_empresa(sender, instance, created, **kwargs):
    """Crea automáticamente el perfil de empresa solo si NO se registró manualmente."""
    # Importamos dentro de la función para evitar el ciclo
    from usuario.models import PerfilEmpresa, Usuario

    # Evita crear si ya existe o si el registro viene del formulario
    if created and instance.rol == Usuario.EMPRESA and not hasattr(instance, 'perfil_empresa'):
        # Solo crea un perfil vacío si es un registro interno, no desde el formulario
        if not PerfilEmpresa.objects.filter(usuario=instance).exists():
            PerfilEmpresa.objects.create(
                usuario=instance,
                razon_social=f"Empresa de {instance.username}",
                nit="TEMPORAL",
                telefono="0000000000",
                sector=None
            )
