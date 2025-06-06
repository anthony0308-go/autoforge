from django import forms
from .models import Repuestos
from decimal import Decimal, ROUND_HALF_UP
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
        error_messages = {
            'nombre_repuesto': {
                'required': 'Campo requerido.'
            },
            'marca_repuesto': {
                'required': 'Campo requerido.'
            },
            'precio_unitario_referencia': {
                'required': 'Campo requerido.'
            },
            'stock': {
                'required': 'Campo requerido.'
            },
        }
        widgets = {
            'nombre_repuesto': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-[#D7141A]',
                'placeholder': 'Nombre del repuesto',
                'required': True,
            }),
            'marca_repuesto': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-[#D7141A]',
                'placeholder': 'Marca del repuesto',
                'required': True,
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-[#D7141A]',
                'placeholder': 'Descripción breve',
                'rows': 3,
            }),
            'precio_unitario_referencia': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-[#D7141A] pl-10',
                'step': '0.01',
                'min': '0',
                'placeholder': '00.00',
                'inputmode': 'decimal',
                'required': True,
                'id': 'id_precio_unitario_referencia',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded focus:outline-none focus:ring focus:border-[#D7141A]',
                'min': '0',
                'value': '1',
                'required': True,
                'id': 'id_stock',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        precio = cleaned_data.get("precio_unitario_referencia")
        stock = cleaned_data.get("stock")

        if precio is None:
            self.add_error("precio_unitario_referencia", "Por favor, indica el precio del repuesto.")
        if stock is None:
            self.add_error("stock", "Por favor, especifica el stock disponible.")

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock

    def clean_precio_unitario_referencia(self):
        precio = self.cleaned_data.get("precio_unitario_referencia")
        if precio is not None:
            if precio < 0:
                raise forms.ValidationError("El precio no puede ser negativo.")
            from decimal import Decimal, ROUND_HALF_UP
            if precio != precio.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):
                raise forms.ValidationError("El precio debe tener como máximo 2 decimales.")
        return precio
   