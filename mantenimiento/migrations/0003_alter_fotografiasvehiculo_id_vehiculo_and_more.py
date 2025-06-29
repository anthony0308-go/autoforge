# Generated by Django 5.0.4 on 2025-06-23 05:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0002_alter_usuarios_dui'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotografiasvehiculo',
            name='id_vehiculo',
            field=models.ForeignKey(db_column='id_vehiculo', on_delete=django.db.models.deletion.DO_NOTHING, to='mantenimiento.vehiculos'),
        ),
        migrations.AlterField(
            model_name='mantenimientorepuestos',
            name='id_mantenimiento',
            field=models.ForeignKey(db_column='id_mantenimiento', on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.mantenimientos'),
        ),
        migrations.AlterField(
            model_name='mantenimientorepuestos',
            name='id_repuesto',
            field=models.ForeignKey(db_column='id_repuesto', on_delete=django.db.models.deletion.CASCADE, to='mantenimiento.repuestos'),
        ),
        migrations.AlterField(
            model_name='vehiculos',
            name='id_usuario_propietario',
            field=models.ForeignKey(db_column='id_usuario_propietario', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
