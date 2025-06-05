from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.shortcuts import render

def inicio(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mantenimiento.urls')),
    path('inicio/', inicio, name='inicio'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)