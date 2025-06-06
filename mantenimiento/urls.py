from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('mantenimientos/', views.listar_mantenimientos, name='listar_mantenimientos'),

    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculo/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculo/<int:vehiculo_id>/mantenimiento/', views.registrar_mantenimiento, name='registrar_mantenimiento'),

    path('repuestos/', views.listar_repuestos, name='listar_repuestos'),
    path('repuestos/registrar/', views.registrar_repuesto, name='registrar_repuesto'),
    path('repuestos/modal/registrar/', views.modal_registrar_repuesto, name='modal_registrar_repuesto'),
    path('repuestos/editar/<int:repuesto_id>/', views.modal_editar_repuesto, name='modal_editar_repuesto'),
    path('repuestos/eliminar/<int:repuesto_id>/', views.eliminar_repuesto, name='eliminar_repuesto'),
    path('repuestos/confirmar_eliminacion/<int:repuesto_id>/', views.modal_confirmar_eliminacion, name='modal_confirmar_eliminacion'),




]
