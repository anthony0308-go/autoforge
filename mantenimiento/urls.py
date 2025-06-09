from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('mantenimientos/', views.listar_mantenimientos, name='listar_mantenimientos'),

    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculo/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculos/registrar/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/<int:vehiculo_id>/editar/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/<int:vehiculo_id>/eliminar/', views.eliminar_vehiculo, name='eliminar_vehiculo'),

    

    path('repuestos/', views.listar_repuestos, name='listar_repuestos'),
    path('repuestos/registrar/', views.registrar_repuesto, name='registrar_repuesto'),
    path('repuestos/modal/registrar/', views.modal_registrar_repuesto, name='modal_registrar_repuesto'),
    path('repuestos/editar/<int:repuesto_id>/', views.modal_editar_repuesto, name='modal_editar_repuesto'),
    path('repuestos/eliminar/<int:repuesto_id>/', views.eliminar_repuesto, name='eliminar_repuesto'),
    path('repuestos/confirmar_eliminacion/<int:repuesto_id>/', views.modal_confirmar_eliminacion, name='modal_confirmar_eliminacion'),

    path('mantenimientos/', views.listar_mantenimientos, name='listar_mantenimientos'),
    path('mantenimientos/crear/', views.crear_mantenimiento, name='crear_mantenimiento'),
    path('mantenimientos/<int:mantenimiento_id>/', views.detalle_mantenimiento, name='detalle_mantenimiento'),
    path('mantenimientos/<int:vehiculo_id>/agendar/', views.agendar_mantenimiento, name='agendar_mantenimiento'),
    path('mantenimientos/agendados/', views.listar_mantenimientos_agendados, name='listar_mantenimientos_agendados'),
    path('mantenimientos/agendar/', views.agendar_mantenimiento, name='agendar_mantenimiento_manual'),

    path('clientes/crear/', views.crear_cliente_y_vehiculo, name='crear_cliente'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
