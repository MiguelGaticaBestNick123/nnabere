from django.contrib import admin
from .models import Ciudad, Prevision, Especialidad, Pacientes, Profesionales, Bloque, Contrato, Box, Agenda, HistorialPago
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Crear grupo de médicos
medicos_group, created = Group.objects.get_or_create(name='Medicos')

# Crear grupo de secretarias
secretarias_group, created = Group.objects.get_or_create(name='Secretarias')


@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombreCiudad',)

@admin.register(Prevision)
class PrevisionAdmin(admin.ModelAdmin):
    list_display = ('nombrePrevision',)

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombreEspecialidad',)

@admin.register(Pacientes)
class PacientesAdmin(admin.ModelAdmin):
    list_display = ('RutPaciente', 'Nombres', 'ApePat', 'ApeMat', 'FechaNac', 'Direccion', 'IdCiudad', 'Cell', 'Email', 'IDPrevision', 'Estado', 'NombreSocial', 'FechaRegistro', 'IdUsuario')

@admin.register(Profesionales)
class ProfesionalesAdmin(admin.ModelAdmin):
    list_display = ('Rut', 'Nombres', 'ApePat', 'ApeMat', 'IDEspecialidad', 'Direccion', 'IdCiudad', 'Cell', 'Email', 'Tarifa', 'Estado', 'FechaRegistro', 'IdUsuario')

@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = ('Descripcion', 'Estado', 'HoraIni', 'HoraFin')

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('FechaContrato', 'RutProfesional', 'Porcentaje', 'Estado', 'FechaIni', 'FechaFIn', 'FechaRegistro', 'IdUsuario')

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('Descripcion', 'ValorMensual', 'FechaRegistro', 'IdUsuario')

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('RutProfesional', 'RutPaciente', 'FechaHoraSolicitud', 'FechaAtencion', 'Estado', 'IdBloque', 'Tarifa', 'IdBox', 'IdContrato')

@admin.register(HistorialPago)
class HistorialPagoAdmin(admin.ModelAdmin):
    list_display = ('FechaHoraPago', 'Mes', 'Año', 'ValorPagoReal', 'ValorACancelar', 'EstadoPago', 'Descripcion', 'FormaPago', 'RutProfesional', 'contrato_idcontrato', 'FechaRegistro', 'IdUsuario')



