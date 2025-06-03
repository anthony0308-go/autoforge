from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm
from .models import Vehiculo

def login_view(request):
    form = CustomLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('mis_vehiculos')  # o cualquier otra vista protegida
    return render(request, 'mantenimiento/login.html', {'form': form})

@login_required
def mis_vehiculos(request):
    vehiculos = Vehiculo.objects.filter(usuario=request.user)
    return render(request, 'mantenimiento/mis_vehiculos.html', {'vehiculos': vehiculos})