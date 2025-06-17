from django import forms
from .models import *
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
import re

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
    first_name = forms.CharField(
        label='Nombre',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'placeholder': 'Apellido'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'placeholder': 'Correo electrónico'
        })
    )
    telefono = forms.CharField(
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'placeholder': 'Teléfono (8 dígitos)'
        })
    )
    dui = forms.CharField(
        label='DUI',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'placeholder': 'DUI'
        })
    )
    direccion = forms.CharField(
        label='Dirección',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'rows': 3,
            'placeholder': 'Dirección'
        })
    )
    password = forms.CharField(
        label='Nueva Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-md bg-transparent border border-gray-300 px-3 py-2',
            'placeholder': 'Deja en blanco para mantener la contraseña actual'
        })
    )

    class Meta:
        model = Usuarios
        fields = ['first_name', 'last_name', 'email', 'telefono', 'dui', 'direccion']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\d{4}-\d{4}$', telefono):
            raise ValidationError("El teléfono debe tener el formato 1234-5678.")
        return telefono

    def clean_dui(self):
        dui = self.cleaned_data.get('dui')
        if dui and not re.match(r'^\d{8}-\d{1}$', dui):
            raise ValidationError("El DUI debe tener el formato 12345678-9.")
        return dui

    def save(self, commit=True):
        usuario = super().save(commit=False)
        nueva_contraseña = self.cleaned_data.get('password')
        if nueva_contraseña:
            usuario.set_password(nueva_contraseña)  # Cifra correctamente la nueva contraseña
        # Si el campo está vacío, NO modifica la contraseña
        if commit:
            usuario.save()
        return usuario


class VehiculoForm(forms.ModelForm):
    tipo_placa = forms.ChoiceField(
        label="Tipo de Placa",
        choices=Vehiculos._meta.get_field('tipo_placa').choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    placa = forms.CharField(
        label="Placa",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'maxlength': 6,
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
            'title': 'La placa debe tener 6 dígitos'
        })
    )
    marca = forms.CharField(
        label="Marca",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    modelo = forms.CharField(
        label="Modelo",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    anio = forms.IntegerField(
        label="Año",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )
    tipo_combustible = forms.CharField(
        label="Tipo de combustible",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    vin = forms.CharField(
        label="VIN",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    color = forms.CharField(
        label="Color",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    foto_frontal = forms.ImageField(
        label="Foto Frontal",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-input'})
    )
    foto_lateral_izquierda = forms.ImageField(
        label="Foto Lateral Izquierda",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-input'})
    )
    foto_lateral_derecha = forms.ImageField(
        label="Foto Lateral Derecha",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-input'})
    )
    foto_trasera = forms.ImageField(
        label="Foto Trasera",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Vehiculos
        exclude = ['id_usuario_propietario', 'id_usuario_registra_vehiculo', 'fecha_registro_vehiculo']
        # No necesitas widgets aquí, ya que todos los campos se declaran arriba con sus widgets y required=False

    def clean(self):
        cleaned_data = super().clean()
        campos_obligatorios = [
            ('tipo_placa', 'Tipo de Placa'),
            ('placa', 'Placa'),
            ('marca', 'Marca'),
            ('modelo', 'Modelo'),
            ('anio', 'Año'),
            ('tipo_combustible', 'Tipo de combustible'),
            ('vin', 'VIN'),
            ('color', 'Color'),
            ('foto_frontal', 'Foto frontal'),
            ('foto_lateral_izquierda', 'Foto lateral izquierda'),
            ('foto_lateral_derecha', 'Foto lateral derecha'),
            ('foto_trasera', 'Foto trasera'),
        ]
        errores = {}
        for campo, label in campos_obligatorios:
            valor = cleaned_data.get(campo)
            if not valor:
                errores[campo] = f'El campo "{label}" es obligatorio.'

        if errores:
            raise forms.ValidationError(errores)
        return cleaned_data

    # Validación adicional opcional en el backend
    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa and not placa.isdigit():
            raise forms.ValidationError("La placa debe contener solo dígitos.")
        if placa and len(placa) != 6:
            raise forms.ValidationError("La placa debe tener exactamente 6 dígitos.")
        return placa
    
    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if vin:
            if not vin.isalnum():
                raise forms.ValidationError("El VIN solo debe contener letras y números.")
            if len(vin) != 17:
                raise forms.ValidationError("El VIN debe tener exactamente 17 caracteres.")
        return vin
        
    