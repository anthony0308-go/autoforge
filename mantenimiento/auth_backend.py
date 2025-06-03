from django.contrib.auth.backends import BaseBackend
from .models import Usuarios
from django.contrib.auth.models import AnonymousUser

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Usuarios.objects.get(email=username)
            if usuario.password_hash == password and usuario.activo:
                return usuario
        except Usuarios.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
