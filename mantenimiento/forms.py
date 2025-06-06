from django import forms
from .models import Repuestos
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.EmailField(label="Correo electrónico", max_length=100, required=True)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Buscar si existe el usuario por email
            try:
                user_obj = User.objects.get(email=username)
            except User.DoesNotExist:
                raise forms.ValidationError("El usuario no existe.")

            # Autenticar con contraseña
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Contraseña incorrecta.")
            if not user.is_active:
                raise forms.ValidationError("Este usuario está inactivo.")

            # Guardar el usuario autenticado para usarlo después
            self.user = user

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuestos
        fields = ['nombre_repuesto', 'marca_repuesto', 'descripcion', 'precio_unitario_referencia', 'stock']
        widgets = {
            'precio_unitario_referencia': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        precio = cleaned_data.get("precio_unitario_referencia")
        stock = cleaned_data.get("stock")

        if precio is None:
            self.add_error("precio_unitario_referencia", "Por favor, indica el precio del repuesto.")

        if stock is None:
            self.add_error("stock", "Por favor, especifica el stock disponible.")
        