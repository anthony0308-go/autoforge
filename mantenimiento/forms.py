from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class CustomLoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.add_error('username', 'Este usuario no existe.')
                return

            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error('password', 'Contraseña incorrecta.')
