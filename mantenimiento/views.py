from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import LoginForm
from .models import Usuarios, Vehiculos, Repuestos, Mantenimientos
from .utils import obtener_usuario_actual


def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        usuario = authenticate(request, username=username, password=password)

        if usuario:
            request.session['usuario_id'] = usuario.id_usuario
            return redirect('inicio')
        else:
            error = "Usuario o contraseña incorrectos."

    return render(request, 'mantenimiento/login.html', {'form': form, 'error': error})


def logout_view(request):
    request.session.flush()
    return redirect('login')


#@login_required
def inicio(request):
    usuario = obtener_usuario_actual(request)
    return render(request, '/mantenimiento/vehiculos/inicio.html', {'usuario': usuario})


#@login_required
def listar_clientes(request):
    clientes = Usuarios.objects.filter(id_rol__nombre_rol='Cliente')
    return render(request, 'mantenimiento/clientes/listar_clientes.html', {'clientes': clientes})


#@login_required
def listar_vehiculos(request):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    vehiculos = Vehiculos.objects.filter(id_usuario_propietario=usuario)
    return render(request, '/mantenimiento/vehiculos/listar.html', {'vehiculos': vehiculos})


#@login_required
def detalle_vehiculo(request, vehiculo_id):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id, id_usuario_propietario=usuario)
    return render(request, '/mantenimiento/vehiculos/detalle.html', {'vehiculo': vehiculo})


#@login_required
def registrar_mantenimiento(request, vehiculo_id):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id, id_usuario_propietario=usuario)
    return render(request, '/mantenimiento/vehiculos/registrar_mantenimiento.html', {'vehiculo': vehiculo})


#@login_required
def listar_mantenimientos(request):
    mantenimientos = Mantenimientos.objects.select_related('id_vehiculo', 'id_usuario')
    return render(request, '/mantenimiento/mantenimientos/listar_mantenimientos.html', {'mantenimientos': mantenimientos})


#@login_required
def listar_repuestos(request):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    repuestos = Repuestos.objects.all()
    return render(request, '/mantenimiento/repuestos/listar.html', {'repuestos': repuestos})
