from django.urls import path
from .views import inicio, agendar, login_view, logout_view, reservas, verificar_rut, registro, datosform, bloques_disponibles, eliminar_reserva, secretaria, agendar_secretaria, contacto, lista_medico, lista_reserva, lista_medico, lista_paciente, datosform_medico, GetBloquesView


urlpatterns = [
    path('', inicio, name="inicio"),
    path ('agendar/', agendar, name="agendar"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reservas/', reservas, name='reservas'),
    path('verificar_rut/', verificar_rut, name='verificar_rut'),
    path('registro/', registro, name='registro'),
    path('datosform/', datosform, name='datosform'),
    path('bloques_disponibles/', bloques_disponibles, name='bloques_disponibles'),
    path('eliminar_reserva/<int:reserva_id>/', eliminar_reserva, name='eliminar_reserva'),
    path('secretaria/', secretaria, name='secretaria'),
    path('agendar_secretaria/', agendar_secretaria, name='agendar_secretaria'),
    path('contacto/', contacto, name='contacto'),
    path('lista_medico/', lista_medico, name='lista_medico'),
    path('lista_reserva/', lista_reserva, name='lista_reserva'),
    path('lista_paciente/', lista_paciente, name='lista_paciente'),
    path('datosform_medico/', datosform_medico, name='datosform_medico'),
    path('/get_bloques/', GetBloquesView.as_view(), name='get_bloques'),
    
]    