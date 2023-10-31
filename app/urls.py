from django.urls import path
from .views import inicio, agendar, login_view, logout_view, reservas, verificar_rut, registro, datosform


urlpatterns = [
    path('', inicio, name="inicio"),
    path ('agendar/', agendar, name="agendar"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reservas/', reservas, name='reservas'),
    path('verificar_rut/', verificar_rut, name='verificar_rut'),
    path('registro/', registro, name='registro'),
    path('datosform/', datosform, name='datosform'),
]    