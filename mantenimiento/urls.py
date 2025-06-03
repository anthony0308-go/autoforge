from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculo/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculo/<int:vehiculo_id>/mantenimiento/', views.registrar_mantenimiento, name='registrar_mantenimiento'),

    path('repuestos/', views.listar_repuestos, name='listar_repuestos'),
]
