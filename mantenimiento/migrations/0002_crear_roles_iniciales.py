from django.db import migrations

def crear_roles(apps, schema_editor):
    Roles = apps.get_model('mantenimiento', 'Roles')
    Roles.objects.get_or_create(nombre_rol='Admin', codigo_rol='A')
    Roles.objects.get_or_create(nombre_rol='Cliente', codigo_rol='C')

class Migration(migrations.Migration):

    dependencies = [
        ('mantenimiento', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_roles),
    ]