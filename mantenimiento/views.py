from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RepuestoForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Usuarios, Vehiculos, Repuestos, Mantenimientos
from .utils import obtener_usuario_actual
from django.core.paginator import Paginator
from django.db.models import Q

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('inicio')
        else:
            # Recoge el mensaje real del formulario
            error = form.errors.get('__all__')
            if error:
                error = error[0]
            else:
                error = "Usuario o contraseña incorrectos."
    return render(request, 'mantenimiento/login.html', {'form': form, 'error': error})



def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def inicio(request):
    usuario = obtener_usuario_actual(request)
    return render(request, 'mantenimiento/inicio.html', {'usuario': usuario})


@login_required
def listar_clientes(request):
    clientes = Usuarios.objects.filter(id_rol__nombre_rol='Cliente')
    return render(request, 'mantenimiento/clientes/listar_clientes.html', {'clientes': clientes})

@login_required
def listar_vehiculos(request):
    usuario = obtener_usuario_actual(request)
    vehiculos = Vehiculos.objects.filter(id_usuario_propietario=usuario)
    return render(request, 'mantenimiento/vehiculos/listar.html', {'vehiculos': vehiculos})

@login_required
def detalle_vehiculo(request, vehiculo_id):
    usuario = obtener_usuario_actual(request)
    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id, id_usuario_propietario=usuario)
    return render(request, 'mantenimiento/vehiculos/detalle.html', {'vehiculo': vehiculo})

@login_required
def registrar_mantenimiento(request, vehiculo_id):
    usuario = obtener_usuario_actual(request)
    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id, id_usuario_propietario=usuario)
    return render(request, 'mantenimiento/vehiculos/registrar_mantenimiento.html', {'vehiculo': vehiculo})

@login_required
def listar_mantenimientos(request):
    mantenimientos = Mantenimientos.objects.select_related('id_vehiculo', 'id_usuario')
    return render(request, 'mantenimiento/mantenimientos/listar_mantenimientos.html', {'mantenimientos': mantenimientos})

# REPUESTOS

@login_required
def listar_repuestos(request):
    repuestos = Repuestos.objects.all()
    return render(request, 'mantenimiento/repuestos/listar_repuestos.html', {'repuestos': repuestos})

@login_required
def registrar_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_repuestos')
    else:
        form = RepuestoForm()
    return render(request, 'mantenimiento/repuestos/registrar_repuesto.html', {'form': form})

@login_required
def modal_registrar_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.location.reload();</script>')
        else:
            # ⚠️ Formulario inválido: lo volvemos a renderizar con errores
            return render(request, 'mantenimiento/repuestos/_form_modal.html', {'form': form})
    else:
        form = RepuestoForm()
        return render(request, 'mantenimiento/repuestos/_form_modal.html', {'form': form})
    

@login_required
def eliminar_repuesto(request, repuesto_id):
    if request.method == 'POST':
        repuesto = get_object_or_404(Repuestos, pk=repuesto_id)
        repuesto.delete()

        # Recalcular los repuestos visibles
        buscar = request.GET.get('buscar', '')
        repuestos = Repuestos.objects.all()
        if buscar:
            repuestos = repuestos.filter(
                Q(nombre_repuesto__icontains=buscar) |
                Q(marca_repuesto__icontains=buscar)
            )

        paginator = Paginator(repuestos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        html = render_to_string('mantenimiento/repuestos/tabla_repuestos.html', {
            'repuestos': page_obj,
            'page_obj': page_obj,
            'buscar': buscar,
        })

        return HttpResponse(html)

    return HttpResponse(status=405)


@login_required
def modal_confirmar_eliminacion(request, repuesto_id):
    repuesto = get_object_or_404(Repuestos, pk=repuesto_id)
    return render(request, 'mantenimiento/repuestos/confirmar_eliminacion.html', {'repuesto': repuesto})


@login_required
def modal_editar_repuesto(request, repuesto_id):
    repuesto = get_object_or_404(Repuestos, pk=repuesto_id)

    if request.method == 'POST':
        form = RepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            return HttpResponse('<script>window.location.reload();</script>')
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, 'mantenimiento/repuestos/editar_form_modal.html', {'form': form, 'repuesto': repuesto})
