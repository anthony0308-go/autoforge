from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .forms import LoginForm  # asume que ya tienes un formulario personalizado
from .models import Vehiculos, Mantenimientos, Repuestos, Usuarios


@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('inicio')  # Cambia a tu ruta principal
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def inicio(request):
    return render(request, 'inicio.html')


@login_required
def listar_vehiculos(request):
    vehiculos = Vehiculos.objects.all()
    return render(request, 'vehiculos/listar.html', {'vehiculos': vehiculos})


@login_required
def detalle_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id)
    mantenimientos = Mantenimientos.objects.filter(id_vehiculo=vehiculo)
    return render(request, 'vehiculos/detalle.html', {
        'vehiculo': vehiculo,
        'mantenimientos': mantenimientos
    })


@login_required
def registrar_mantenimiento(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id)
    if request.method == 'POST':
        # lógica para guardar el mantenimiento desde un formulario
        pass
    return render(request, 'mantenimientos/registrar.html', {'vehiculo': vehiculo})


@login_required
def listar_repuestos(request):
    repuestos = Repuestos.objects.all()
    return render(request, 'repuestos/listar.html', {'repuestos': repuestos})

