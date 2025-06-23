from django.core.management.base import BaseCommand
from mantenimiento.models import Usuarios, Roles
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Crea un usuario seleccionando rol por código (A/C)'

    def handle(self, *args, **options):
        print('\n--- Crear usuario en AutoForge ---\n')
        email = input('Correo electrónico: ').strip()
        first_name = input('Nombre: ').strip()
        last_name = input('Apellidos: ').strip()

        # Pedir y validar DUI (obligatorio y único)
        while True:
            dui = input('DUI (sin guiones): ').strip()
            if not dui:
                print("⚠️  El DUI es obligatorio.")
            elif Usuarios.objects.filter(dui=dui).exists():
                print("⚠️  Ya existe un usuario con ese DUI.")
            else:
                break

        # Mostrar roles disponibles
        print('\nRoles disponibles:')
        for rol in Roles.objects.all():
            print(f"  [{rol.codigo_rol}] {rol.nombre_rol}")

        # Solicitar código de rol y validar
        while True:
            codigo_rol = input('Código de rol (A/C): ').strip().upper()
            try:
                rol = Roles.objects.get(codigo_rol=codigo_rol)
                break
            except ObjectDoesNotExist:
                print("Código inválido. Elige un código válido de la lista.")

        password = input('Contraseña: ').strip()

        try:
            usuario = Usuarios.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                dui=dui,
                id_rol=rol
            )
            if codigo_rol == 'A':
                usuario.is_superuser = True
                usuario.is_staff = True
                usuario.save()
                self.stdout.write(self.style.SUCCESS('✅ Usuario administrador creado exitosamente.'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ Usuario cliente creado exitosamente.'))
        except IntegrityError as e:
            self.stderr.write(self.style.ERROR(f"❌ Error de integridad al crear el usuario: {str(e)}"))
