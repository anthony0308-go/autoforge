from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

from autoforge_core import settings
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import *
from .utils import obtener_usuario_actual
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.forms import inlineformset_factory
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives


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
    vehiculo = get_object_or_404(Vehiculos, pk=vehiculo_id)
    mantenimientos = Mantenimientos.objects.filter(id_vehiculo=vehiculo).order_by('-fecha_ingreso')
    return render(request, 'vehiculos/detalle_vehiculo.html', {
        'vehiculo': vehiculo,
        'mantenimientos': mantenimientos,
    })


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

    return render(request, 'mantenimiento/repuestos/listar_repuestos.html', {
        'repuestos': page_obj,
        'buscar': buscar,
        'page_obj': page_obj,
    })


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
        return HttpResponse(status=204, headers={"HX-Refresh": "true"})
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


#VIEWS PARA MANTENIMIENTOS  
@login_required
def crear_mantenimiento(request):
    MantenimientoRepuestoFormSet = inlineformset_factory(
        Mantenimientos,
        MantenimientoRepuestos,
        form=MantenimientoRepuestoForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        formset = MantenimientoRepuestoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                mantenimiento = form.save(commit=False)
                mantenimiento.id_usuario_abre_orden = request.user
                mantenimiento.save()

                total_repuestos = 0
                for f in formset:
                    if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                        cantidad = f.cleaned_data['cantidad_utilizada'] or 0
                        precio = f.cleaned_data['precio_unitario_al_momento'] or 0
                        subtotal = cantidad * float(precio)
                        total_repuestos += subtotal

                        repuesto = f.save(commit=False)
                        repuesto.id_mantenimiento = mantenimiento
                        repuesto.subtotal = subtotal
                        repuesto.save()

                # Totales
                mano_obra = form.cleaned_data.get('costo_mano_obra') or 0
                otros = form.cleaned_data.get('otros_cargos') or 0
                desc = form.cleaned_data.get('descuentos') or 0
                mantenimiento.costo_total_repuestos = total_repuestos
                mantenimiento.costo_total_mantenimiento = mano_obra + total_repuestos + otros - desc
                mantenimiento.save()

                # 🔔 Enviar correo tipo factura
                vehiculo = mantenimiento.id_vehiculo
                cliente = vehiculo.id_usuario_propietario
                if cliente and cliente.email:
                    repuestos_usados = MantenimientoRepuestos.objects.filter(id_mantenimiento=mantenimiento)

                    contexto = {
                        'cliente': cliente,
                        'mantenimiento': mantenimiento,
                        'repuestos': repuestos_usados,
                    }

                    asunto = f"[AutoForge] Factura del mantenimiento realizado - {vehiculo.placa}"
                    cuerpo_html = render_to_string("emails/factura_mantenimiento.html", contexto)
                    cuerpo_texto = (
                        f"Estimado {cliente.first_name},\n\n"
                        f"Adjuntamos los detalles del mantenimiento realizado a su vehículo {vehiculo.placa}.\n"
                        f"Gracias por confiar en AutoForge."
                    )

                    correo = EmailMultiAlternatives(
                        subject=asunto,
                        body=cuerpo_texto,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[cliente.email],
                    )
                    correo.attach_alternative(cuerpo_html, "text/html")
                    correo.send()

            return redirect('listar_mantenimientos')
    else:
        now = timezone.localtime().strftime("%Y-%m-%dT%H:%M")
        form = MantenimientoForm(initial={'fecha_ingreso': now})
        formset = MantenimientoRepuestoFormSet()

    return render(request, 'mantenimiento/mantenimientos/crear_mantenimiento.html', {
        'form': form,
        'formset': formset,
    })



@login_required
def listar_mantenimientos(request):
    if request.user.id_rol.codigo_rol == 'A':  # admin
        mantenimientos = Mantenimientos.objects.all().order_by('-fecha_ingreso')
    else:
        # Cliente: solo los de sus vehículos
        vehiculos_usuario = Vehiculos.objects.filter(id_usuario_propietario=request.user)
        mantenimientos = Mantenimientos.objects.filter(id_vehiculo__in=vehiculos_usuario).order_by('-fecha_ingreso')

    buscar = request.GET.get('buscar', '')
    if buscar:
        mantenimientos = mantenimientos.filter(
            Q(id_vehiculo__placa__icontains=buscar) | 
            Q(id_tipo_mantenimiento__nombre_tipo__icontains=buscar)
        )

    paginator = Paginator(mantenimientos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mantenimiento/mantenimientos/listar_mantenimientos.html', {
        'mantenimientos': page_obj,
        'buscar': buscar,
        'page_obj': page_obj,
    })


@login_required
def agendar_mantenimiento(request, vehiculo_id=None):
    initial = {}
    if vehiculo_id:
        initial['id_vehiculo'] = vehiculo_id

    if request.method == 'POST':
        form = MantenimientoAgendadoForm(request.POST, initial=initial)
        if form.is_valid():
            agendado = form.save(commit=False)
            agendado.id_usuario_agenda = request.user
            agendado.save()

            # 🔔 Enviar correo al dueño del vehículo
            vehiculo = agendado.id_vehiculo
            propietario = vehiculo.id_usuario_propietario
            if propietario and propietario.email:
                asunto = f"[AutoForge] Mantenimiento programado para {vehiculo.placa}"
                mensaje = (
                    f"Hola {propietario.first_name},\n\n"
                    f"Se ha programado un mantenimiento para tu vehículo:\n\n"
                    f"Vehículo: {vehiculo.marca} {vehiculo.modelo} ({vehiculo.placa})\n"
                    f"Fecha programada: {agendado.fecha_programada}\n"
                    f"Tipo sugerido: {agendado.id_tipo_mantenimiento_sugerido or 'General'}\n"
                    f"Kilometraje estimado: {agendado.kilometraje_programado or 'N/D'} km\n"
                    f"Notas: {agendado.notas or 'Sin notas'}\n\n"
                    f"Nos vemos en el taller AutoForge. ¡Gracias por confiar en nosotros!"
                )
                send_mail(
                    subject=asunto,
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[propietario.email],
                    fail_silently=False,
                )

            return redirect('listar_mantenimientos_agendados')
    else:
        form = MantenimientoAgendadoForm(initial=initial)

    return render(request, 'mantenimiento/mantenimientos/agendar_mantenimiento.html', {
        'form': form
    })


@login_required
def listar_mantenimientos_agendados(request):
    if request.user.id_rol.codigo_rol == 'A':
        agendados = MantenimientosAgendados.objects.all().order_by('-fecha_programada')
    else:
        vehiculos_usuario = Vehiculos.objects.filter(id_usuario_propietario=request.user)
        agendados = MantenimientosAgendados.objects.filter(id_vehiculo__in=vehiculos_usuario).order_by('-fecha_programada')

    return render(request, 'mantenimiento/mantenimientos/listar_agendados.html', {'agendados': agendados})


@login_required
def detalle_mantenimiento(request, mantenimiento_id):
    mantenimiento = get_object_or_404(Mantenimientos, pk=mantenimiento_id)
    repuestos = MantenimientoRepuestos.objects.filter(id_mantenimiento=mantenimiento)
    # Puedes agregar control de roles si quieres limitar qué usuarios pueden ver este detalle.
    return render(request, 'mantenimiento/mantenimientos/detalle_mantenimiento.html', {
        'mantenimiento': mantenimiento,
        'repuestos': repuestos,
    })

@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Usuarios, pk=cliente_id)
    vehiculos = cliente.vehiculos_set.all()
    mantenimientos = Mantenimientos.objects.filter(id_vehiculo__id_usuario_propietario=cliente).order_by('-fecha_ingreso')

    return render(request, 'clientes/detalle_cliente.html', {
        'cliente': cliente,
        'vehiculos': vehiculos,
        'mantenimientos': mantenimientos,
    })
