from django.contrib import admin
from .models import Vehiculo, Mantenimiento, TipoMantenimiento, Repuesto

# Register your models here.
admin.site.site_header = "AutoForge 🚗 Panel de Administración"
admin.site.site_title = "AutoForge Admin"
admin.site.index_title = "Bienvenido al administrador de AutoForge"


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'año', 'color', 'usuario')
    search_fields = ('placa', 'marca', 'modelo', 'usuario__username')
    list_filter = ('año', 'marca')

@admin.register(TipoMantenimiento)
class TipoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_unitario', 'marca')
    search_fields = ('nombre', 'codigo', 'marca')

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'tipo', 'fecha', 'costo_total')
    search_fields = ('vehiculo__placa', 'tipo')
    list_filter = ('fecha',)
    readonly_fields = ('costo_total',)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # guarda el objeto
        if 'repuestos' in form.cleaned_data:
            total = sum(r.precio_unitario for r in form.cleaned_data['repuestos'])
            obj.costo_total = total
            obj.save(update_fields=['costo_total'])