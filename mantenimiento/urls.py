from django.urls import path
from . import views
from .views import login_view
# from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    #path('login/', LoginView.as_view(template_name='mantenimiento/login.html'), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('mis-vehiculos/', views.mis_vehiculos, name='mis_vehiculos'),
]
