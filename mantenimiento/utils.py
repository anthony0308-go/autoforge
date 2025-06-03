from .models import Usuarios

def obtener_usuario_actual(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            return Usuarios.objects.get(pk=usuario_id)
        except Usuarios.DoesNotExist:
            return None
    return None
