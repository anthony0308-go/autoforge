from django import forms
from django.contrib.auth.forms import authenticate

class LoginForm(forms.Form):
    username = forms.EmailField(label="Correo electrónico", max_length=100, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        # Solo verifica credenciales si ambos campos están presentes
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")
            if not user.is_active:
                raise forms.ValidationError("Este usuario está inactivo.")
            # Puedes guardar el usuario autenticado si lo necesitas después
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
