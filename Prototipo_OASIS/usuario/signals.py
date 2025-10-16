from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='usuario.Usuario')
def crear_perfil_empresa(sender, instance, created, **kwargs):
    """Crea automáticamente el perfil de empresa al registrarse."""
    # Importamos dentro de la función para evitar el ciclo
    from usuario.models import PerfilEmpresa, Usuario

    if created and instance.rol == Usuario.EMPRESA and not hasattr(instance, 'perfil_empresa'):
        PerfilEmpresa.objects.create(
            usuario=instance,
            razon_social=f"Empresa de {instance.username}",
            nit="PENDIENTE",
            telefono="0000000000",
            sector=None
        )