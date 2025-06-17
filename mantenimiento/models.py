from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager



class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(unique=True, max_length=50)
    codigo_rol = models.CharField(max_length=1, unique=True)

    def __str__(self):
        return f"{self.nombre_rol} ({self.codigo_rol})"

    class Meta:
        db_table = 'roles'

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class Usuarios(AbstractUser):
    id_rol = models.ForeignKey(Roles, on_delete=models.DO_NOTHING, db_column='id_rol', null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    dui = models.CharField(unique=True, max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    carnet_empleado = models.CharField(unique=True, max_length=50, blank=True, null=True)
    fecha_creacion_usuario = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    username = None
    email = models.EmailField('email address', unique=True, max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'id_rol']
    objects = UsuarioManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'usuarios'

    

class FotografiasVehiculo(models.Model):
    id_fotografia = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='id_vehiculo')
    url_fotografia = models.ImageField(upload_to='vehiculos/')
    tipo_fotografia = models.CharField(max_length=20)
    descripcion_foto = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(blank=True, null=True)
    id_usuario_sube_foto = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_sube_foto', blank=True, null=True)

    def __str__(self):
        return str(self.tipo_fotografia)

    class Meta:
        managed = True
        db_table = 'fotografias_vehiculo'


class MantenimientoRepuestos(models.Model):
    id_mantenimiento_repuesto = models.AutoField(primary_key=True)
    id_mantenimiento = models.ForeignKey('Mantenimientos', models.CASCADE, db_column='id_mantenimiento')
    id_repuesto = models.ForeignKey('Repuestos', models.CASCADE, db_column='id_repuesto')
    cantidad_utilizada = models.IntegerField()
    precio_unitario_al_momento = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_usuario_agrega_repuesto = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_agrega_repuesto', blank=True, null=True)

    def __str__(self):
        return str(self.id_repuesto)

    class Meta:
        managed = True
        db_table = 'mantenimiento_repuestos'


class Mantenimientos(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='id_vehiculo')
    id_tipo_mantenimiento = models.ForeignKey('TiposMantenimiento', models.DO_NOTHING, db_column='id_tipo_mantenimiento', blank=True, null=True)
    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(blank=True, null=True)
    fecha_proximo_mantenimiento_preventivo = models.DateField(blank=True, null=True)
    descripcion_problema_cliente = models.TextField(blank=True, null=True)
    diagnostico_taller = models.TextField(blank=True, null=True)
    trabajos_realizados = models.TextField(blank=True, null=True)
    observaciones_mantenimiento = models.TextField(blank=True, null=True)
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_total_repuestos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    otros_cargos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descuentos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_total_mantenimiento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    kilometraje_actual = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    id_usuario_abre_orden = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_abre_orden', blank=True, null=True)
    id_usuario_mecanico_asignado = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_mecanico_asignado', related_name='mantenimientos_id_usuario_mecanico_asignado_set', blank=True, null=True)

    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento} - Vehículo {self.id_vehiculo}"

    class Meta:
        managed = True
        db_table = 'mantenimientos'


class MantenimientosAgendados(models.Model):
    id_mantenimiento_agendado = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='id_vehiculo')
    id_tipo_mantenimiento_sugerido = models.ForeignKey('TiposMantenimiento', models.DO_NOTHING, db_column='id_tipo_mantenimiento_sugerido', blank=True, null=True)
    fecha_programada = models.DateField()
    kilometraje_programado = models.IntegerField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    estado_agendamiento = models.CharField(max_length=50, blank=True, null=True)
    id_mantenimiento_realizado = models.ForeignKey(Mantenimientos, models.DO_NOTHING, db_column='id_mantenimiento_realizado', blank=True, null=True)
    id_usuario_agenda = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario_agenda', blank=True, null=True)
    fecha_creacion_agenda = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Agendado {self.fecha_programada} para {self.id_vehiculo}"

    class Meta:
        managed = True
        db_table = 'mantenimientos_agendados'


class Repuestos(models.Model):
    id_repuesto = models.AutoField(primary_key=True)
    nombre_repuesto = models.CharField(unique=True, max_length=150)
    marca_repuesto = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_unitario_referencia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre_repuesto

    class Meta:
        db_table = 'repuestos'



class TiposMantenimiento(models.Model):
    id_tipo_mantenimiento = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_tipo

    class Meta:
        managed = True
        db_table = 'tipos_mantenimiento'


TIPOS_PLACA = [
    ("P", "Vehículo particular"),
    ("A", "Vehículo de alquiler"),
    ("AB", "Autobús"),
    ("C", "Vehículo de carga"),
    ("M", "Motocicleta particular"),
    ("H", "Vehículo del Estado"),
    ("N", "Vehículo de instituciones autónomas"),
    ("O", "Organismo internacional"),
    ("CD", "Cuerpo diplomático"),
    ("CC", "Cuerpo consular"),
    ("MI", "Misión internacional"),
    ("U", "Uso municipal"),
    ("E", "Vehículo escolar"),
    ("T", "Transporte público (colectivo)"),
    ("TC", "Transporte de carga comercial"),
    ("R", "Remolque"),
    ("TR", "Tractor o maquinaria agrícola/industrial"),
    ("F", "Fuerza Armada"),
    ("D", "Vehículo en demostración (agencia/concesionario)"),
    ("Z", "Vehículo de zona franca o especial"),
    ("B", "Mototaxi / Tricimoto / Bicimoto"),
    ("V", "Vehículo temporal o de visitante"),
    ("POL", "POLIZA (Placa provisional)"),
]

class Vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_usuario_propietario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario_propietario')
    placa = models.CharField(unique=True, max_length=10)
    tipo_placa = models.CharField(max_length=4, choices=TIPOS_PLACA, default="P")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(blank=True, null=True)
    tipo_combustible = models.CharField(max_length=50, blank=True, null=True)
    vin = models.CharField(unique=True, max_length=17, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    fecha_registro_vehiculo = models.DateTimeField(blank=True, null=True)
    id_usuario_registra_vehiculo = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario_registra_vehiculo', related_name='vehiculos_id_usuario_registra_vehiculo_set', blank=True, null=True)

    def __str__(self):
        return self.placa

    class Meta:
        managed = True
        db_table = 'vehiculos'