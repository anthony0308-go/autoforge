import django.db.models.deletion
import django.utils.timezone
import mantenimiento.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FotografiasVehiculo',
            fields=[
                ('id_fotografia', models.AutoField(primary_key=True, serialize=False)),
                ('url_fotografia', models.TextField()),
                ('tipo_fotografia', models.CharField(max_length=20)),
                ('descripcion_foto', models.TextField(blank=True, null=True)),
                ('fecha_subida', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'fotografias_vehiculo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MantenimientoRepuestos',
            fields=[
                ('id_mantenimiento_repuesto', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_utilizada', models.IntegerField()),
                ('precio_unitario_al_momento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'mantenimiento_repuestos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mantenimientos',
            fields=[
                ('id_mantenimiento', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_ingreso', models.DateTimeField()),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('fecha_proximo_mantenimiento_preventivo', models.DateField(blank=True, null=True)),
                ('descripcion_problema_cliente', models.TextField(blank=True, null=True)),
                ('diagnostico_taller', models.TextField(blank=True, null=True)),
                ('trabajos_realizados', models.TextField(blank=True, null=True)),
                ('observaciones_mantenimiento', models.TextField(blank=True, null=True)),
                ('costo_mano_obra', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('costo_total_repuestos', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('otros_cargos', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('descuentos', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('costo_total_mantenimiento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('kilometraje_actual', models.IntegerField(blank=True, null=True)),
                ('estado', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'mantenimientos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MantenimientosAgendados',
            fields=[
                ('id_mantenimiento_agendado', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_programada', models.DateField()),
                ('kilometraje_programado', models.IntegerField(blank=True, null=True)),
                ('notas', models.TextField(blank=True, null=True)),
                ('estado_agendamiento', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_creacion_agenda', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mantenimientos_agendados',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Repuestos',
            fields=[
                ('id_repuesto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_repuesto', models.CharField(max_length=150, unique=True)),
                ('marca_repuesto', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio_unitario_referencia', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'repuestos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TiposMantenimiento',
            fields=[
                ('id_tipo_mantenimiento', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tipos_mantenimiento',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vehiculos',
            fields=[
                ('id_vehiculo', models.AutoField(primary_key=True, serialize=False)),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('anio', models.IntegerField(blank=True, null=True)),
                ('tipo_combustible', models.CharField(blank=True, max_length=50, null=True)),
                ('vin', models.CharField(blank=True, max_length=17, null=True, unique=True)),
                ('color', models.CharField(blank=True, max_length=30, null=True)),
                ('fecha_registro_vehiculo', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'vehiculos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_rol', models.CharField(max_length=50, unique=True)),
                ('codigo_rol', models.CharField(max_length=1, unique=True)),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('dui', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('carnet_empleado', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('fecha_creacion_usuario', models.DateTimeField(auto_now_add=True, null=True)),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('id_rol', models.ForeignKey(db_column='id_rol', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mantenimiento.roles')),
            ],
            options={
                'db_table': 'usuarios',
            },
            managers=[
                ('objects', mantenimiento.models.UsuarioManager()),
            ],
        ),
    ]
