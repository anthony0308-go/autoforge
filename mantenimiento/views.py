from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import LoginForm
from .models import Usuarios, Vehiculos
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


def listar_vehiculos(request):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')
    
    vehiculos = Vehiculos.objects.filter(id_usuario_propietario=usuario)
    return render(request, 'vehiculos/listar.html', {'vehiculos': vehiculos})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def inicio(request):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')
    return render(request, 'inicio.html', {'usuario': usuario})

def detalle_vehiculo(request, vehiculo_id):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id, id_usuario_propietario=usuario)
    return render(request, 'vehiculos/detalle.html', {'vehiculo': vehiculo})

def registrar_mantenimiento(request, vehiculo_id):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id, id_usuario_propietario=usuario)
    return render(request, 'vehiculos/registrar_mantenimiento.html', {'vehiculo': vehiculo})

def listar_repuestos(request):
    usuario = obtener_usuario_actual(request)
    if not usuario:
        return redirect('login')

    repuestos = Repuestos.objects.all()
    return render(request, 'repuestos/listar.html', {'repuestos': repuestos})
