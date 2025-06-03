from django import forms
from .models import Usuarios

class LoginForm(forms.Form):
    username = forms.CharField(label="Correo", max_length=100, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                usuario = Usuarios.objects.get(email=username)
            except Usuarios.DoesNotExist:
                self.add_error('username', 'Este usuario no existe.')
                return

            if not usuario.activo:
                self.add_error('username', 'Este usuario está inactivo.')
                return

            if usuario.password_hash != password:
                self.add_error('password', 'Contraseña incorrecta.')
