from django import forms
from .models import *
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
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
    


# Form principal de mantenimiento
class MantenimientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza la opción vacía del select
        self.fields['id_vehiculo'].empty_label = "Seleccionar vehículo"
        self.fields['id_tipo_mantenimiento'].empty_label = "Seleccionar tipo de mantenimiento"

    class Meta:
        model = Mantenimientos
        fields = [
            'id_vehiculo', 'id_tipo_mantenimiento', 'fecha_ingreso', 'kilometraje_actual',
            'descripcion_problema_cliente', 'diagnostico_taller', 'trabajos_realizados',
            'observaciones_mantenimiento', 'costo_mano_obra', 'otros_cargos', 'descuentos'
        ]
        widgets = {
            'id_vehiculo': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400'}),
            'id_tipo_mantenimiento': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400'}),
            'fecha_ingreso': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400'}),
            'kilometraje_actual': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400'}),
            'descripcion_problema_cliente': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'rows': 2}),
            'diagnostico_taller': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'rows': 2}),
            'trabajos_realizados': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'rows': 2}),
            'observaciones_mantenimiento': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'rows': 2}),
            'costo_mano_obra': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'min': 0, 'step': '0.01'}),
            'otros_cargos': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'min': 0, 'step': '0.01'}),
            'descuentos': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:ring focus:border-blue-400', 'min': 0, 'step': '0.01'}),
        }

class MantenimientoRepuestoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoRepuestos
        fields = ['id_repuesto', 'cantidad_utilizada', 'precio_unitario_al_momento']
        widgets = {
            'id_repuesto': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1'}),
            'cantidad_utilizada': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1', 'min': 1}),
            'precio_unitario_al_momento': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-2 py-1', 'min': 0, 'step': '0.01'}),
        }

#MantenimientosProximos
class MantenimientoAgendadoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_vehiculo'].empty_label = "Seleccionar vehículo"
        self.fields['id_tipo_mantenimiento_sugerido'].empty_label = "Seleccionar tipo de mantenimiento"
    class Meta:
        model = MantenimientosAgendados
        fields = [
            'id_vehiculo', 'id_tipo_mantenimiento_sugerido', 'fecha_programada', 'kilometraje_programado', 'notas'
        ]
        widgets = {
            'fecha_programada': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'kilometraje_programado': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'notas': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 2}),
        }




#ClienteForm y VehiculoForm

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['first_name', 'last_name', 'email', 'telefono', 'dui', 'direccion']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
                'placeholder': 'Correo electrónico'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
                'placeholder': 'Teléfono (8 dígitos)'
            }),
            'dui': forms.TextInput(attrs={
                'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
                'placeholder': 'DUI'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
                'rows': 3,
                'placeholder': 'Dirección'
            }),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and (not telefono.isdigit() or len(telefono) != 8):
            raise ValidationError("El teléfono debe contener exactamente 8 dígitos.")
        return telefono

    def save(self, commit=True):
        instance = super().save(commit=False)
        rol_cliente = Roles.objects.get(codigo_rol='C')
        instance.id_rol = rol_cliente

        instance.username = None  


        if commit:
            instance.save()
        return instance


class VehiculoForm(forms.ModelForm):
    foto_frontal = forms.ImageField(required=True, label="Foto Frontal")
    foto_lateral_izquierda = forms.ImageField(required=True, label="Foto Lateral Izquierda")
    foto_lateral_derecha = forms.ImageField(required=True, label="Foto Lateral Derecha")
    foto_trasera = forms.ImageField(required=True, label="Foto Trasera")

    class Meta:
        model = Vehiculos
        exclude = ['id_usuario_propietario', 'id_usuario_registra_vehiculo', 'fecha_registro_vehiculo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-input'}),
            'marca': forms.TextInput(attrs={'class': 'form-input'}),
            'modelo': forms.TextInput(attrs={'class': 'form-input'}),
            'anio': forms.NumberInput(attrs={'class': 'form-input'}),
            'tipo_combustible': forms.TextInput(attrs={'class': 'form-input'}),
            'vin': forms.TextInput(attrs={'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input'}),
        }

