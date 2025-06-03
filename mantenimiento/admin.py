from django.contrib import admin
from .models import (
    Usuarios, Roles, Vehiculos, TiposMantenimiento,
    Mantenimientos, MantenimientoRepuestos, Repuestos,
    MantenimientosAgendados, FotografiasVehiculo
)
#TODO ESTO LO AÑADI PAL AKMIN
@admin.register(Usuarios)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_completo', 'email', 'telefono', 'activo', 'id_rol')
    list_filter = ('activo', 'id_rol')
    search_fields = ('nombre_completo', 'email', 'dui', 'carnet_empleado')
    ordering = ('-fecha_creacion_usuario',)

@admin.register(Roles)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol')
    search_fields = ('nombre_rol',)

@admin.register(Vehiculos)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id_vehiculo', 'placa', 'marca', 'modelo', 'anio', 'id_usuario_propietario')
    list_filter = ('marca', 'anio', 'tipo_combustible')
    search_fields = ('placa', 'vin', 'marca', 'modelo')
    ordering = ('-fecha_registro_vehiculo',)

@admin.register(TiposMantenimiento)
class TipoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_mantenimiento', 'nombre_tipo')
    search_fields = ('nombre_tipo',)

@admin.register(Mantenimientos)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id_mantenimiento', 'id_vehiculo', 'fecha_ingreso', 'estado', 'costo_total_mantenimiento')
    list_filter = ('estado', 'fecha_ingreso', 'id_tipo_mantenimiento')
    search_fields = ('id_vehiculo__placa', 'diagnostico_taller')
    date_hierarchy = 'fecha_ingreso'

@admin.register(MantenimientoRepuestos)
class MantenimientoRepuestosAdmin(admin.ModelAdmin):
    list_display = ('id_mantenimiento_repuesto', 'id_mantenimiento', 'id_repuesto', 'cantidad_utilizada', 'subtotal')
    search_fields = ('id_mantenimiento__id_vehiculo__placa', 'id_repuesto__nombre_repuesto')

@admin.register(Repuestos)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('id_repuesto', 'nombre_repuesto', 'marca_repuesto', 'precio_unitario_referencia', 'stock')
    list_filter = ('marca_repuesto',)
    search_fields = ('nombre_repuesto',)

@admin.register(MantenimientosAgendados)
class MantenimientoAgendadoAdmin(admin.ModelAdmin):
    list_display = ('id_mantenimiento_agendado', 'id_vehiculo', 'fecha_programada', 'estado_agendamiento')
    list_filter = ('estado_agendamiento',)
    date_hierarchy = 'fecha_programada'

@admin.register(FotografiasVehiculo)
class FotografiasVehiculoAdmin(admin.ModelAdmin):
    list_display = ('id_fotografia', 'id_vehiculo', 'tipo_fotografia', 'fecha_subida')
    search_fields = ('id_vehiculo__placa', 'tipo_fotografia')
