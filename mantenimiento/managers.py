from django.contrib.auth.models import BaseUserManager
from django.apps import apps  # <- Importamos apps para carga dinámica

#TIDI ESTI POR Y PARA EL ADMIN, VIVA EL ADMIN
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, id_rol=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")

        email = self.normalize_email(email)

        # Importación diferida
        Roles = apps.get_model('mantenimiento', 'Roles')

        if id_rol is not None:
            try:
                rol = Roles.objects.get(pk=id_rol)
            except Roles.DoesNotExist:
                raise ValueError('Rol no válido')
        else:
            rol = None

        user = self.model(
            email=email,
            id_rol=rol,
            **extra_fields
        )
        user.set_password(password)
        user.activo = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, id_rol=1, **extra_fields)
