from django.urls import path
from .views import inicio, agendar, login_view, logout_view, reservas, verificar_rut


urlpatterns = [
    path('', inicio, name="inicio"),
    path ('agendar/', agendar, name="agendar"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reservas/', reservas, name='reservas'),
    path('verificar_rut/', verificar_rut, name='verificar_rut'),
]    