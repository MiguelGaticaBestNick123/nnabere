from django.db import models
from django.contrib.auth.models import User

def is_secretaria(self):
    return self.groups.filter(name='Secretarias').exists()

User.add_to_class('is_secretaria', is_secretaria)

def is_medico(self):
    return self.groups.filter(name='Medicos').exists()

User.add_to_class('is_medico', is_medico)

class Ciudad(models.Model):
    nombreCiudad = models.CharField(max_length=50)
    def __str__(self):
        return self.nombreCiudad
class Prevision(models.Model):
    nombrePrevision = models.CharField(max_length=50)
    def __str__(self):
        return self.nombrePrevision

class Especialidad(models.Model):
    nombreEspecialidad = models.CharField(max_length=50)
    def __str__(self):
        return self.nombreEspecialidad

class Pacientes(models.Model):
    RutPaciente = models.CharField(max_length=20, verbose_name='Rut del paciente', primary_key=True, unique=True)
    Nombres = models.CharField(max_length=50, verbose_name='Nombres del paciente')
    ApePat = models.CharField(max_length=50, verbose_name='Apellido paterno del paciente')
    ApeMat = models.CharField(max_length=50, verbose_name='Apellido materno del paciente')
    OrdenAp = models.IntegerField(choices=[(1, 'Apellido Paterno'), (2, 'Apellido Materno')], verbose_name='Orden de apellidos')
    FechaNac = models.DateField(verbose_name='Fecha de nacimiento del paciente', blank=True, null=True)
    Direccion = models.CharField(max_length=100, verbose_name='Dirección del paciente', blank=True, null=True)
    IdCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    Cell = models.CharField(max_length=20, verbose_name='Número de celular del paciente', blank=True, null=True)
    Email = models.EmailField(verbose_name='Correo electrónico del paciente', blank=True, null=True)
    IDPrevision = models.ForeignKey(Prevision, on_delete=models.CASCADE)    
    Estado = models.CharField(max_length=100, verbose_name='Estado del paciente', blank=True, null=True)
    NombreSocial = models.CharField(max_length=100, verbose_name='Nombre social del paciente', blank=True, null=True)
    FechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del paciente', blank=True, null=True)
    IdUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.RutPaciente

class Profesionales(models.Model):
    Rut = models.CharField(max_length=20, verbose_name='Rut del profesional', unique=True, primary_key=True)
    Nombres = models.CharField(max_length=50, verbose_name='Nombres del profesional')
    ApePat = models.CharField(max_length=50, verbose_name='Apellido paterno del profesional')
    ApeMat = models.CharField(max_length=50, verbose_name='Apellido materno del profesional')
    IDEspecialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='especialidad_profesional')
    Direccion = models.CharField(max_length=100, verbose_name='Dirección del profesional')
    IdCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    Cell = models.CharField(max_length=20, verbose_name='Número de celular del profesional')
    Email = models.EmailField(verbose_name='Correo electrónico del profesional')
    Tarifa = models.IntegerField( null=True, default=25000, verbose_name='Tarifa por hora del profesional')
    Estado = models.BooleanField(verbose_name='Estado del profesional')
    FechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del profesional')
    IdUsuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.Rut

class Bloque(models.Model):
    RutProfesional     	=  	models.ForeignKey(Profesionales, on_delete=models.CASCADE, verbose_name="Rut del profesional", related_name='RutProfesional_bloque')	
    Descripcion = models.CharField(max_length=100)
    Estado = models.BooleanField()
    HoraIni = models.TimeField()
    HoraFin = models.TimeField()
    def __str__(self):
        return self.Descripcion

class Contrato(models.Model):
	FechaContrato  	=  	models.DateField(verbose_name='Fecha del contrato')	
	RutProfesional     	=  	models.ForeignKey(Profesionales, on_delete=models.CASCADE, verbose_name="Rut del profesional", related_name='contrato_profesional')	
	Porcentaje     	    =  	models.DecimalField(decimal_places=2, max_digits=10)
	Estado         	    =  	models.BooleanField(verbose_name='Estado del contrato')	
	FechaIni       	    =  	models.DateField(verbose_name='Fecha de inicio del contrato')	
	FechaFIn       	    =  	models.DateField(verbose_name='Fecha de fin del contrato')	
	FechaRegistro 	    =  	models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del contrato')	
	IdUsuario      	    =  	models.ForeignKey(User, on_delete=models.CASCADE)

class Box(models.Model):
    Descripcion    	=  	models.TextField(blank=True, null=True, max_length=100)	
    ValorMensual  	=  	models.DecimalField(decimal_places=2, max_digits=10)	
    FechaRegistro  	=  	models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro de la caja')	
    Estado = models.BooleanField(null=True, default=True)
    def __str__(self):
        return self.Descripcion
class Agenda(models.Model):
    RutProfesional = models.ForeignKey(Profesionales, on_delete=models.CASCADE, related_name='profesional', verbose_name="Rut del profesional", null=True)
    RutPaciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, related_name='paciente', verbose_name="Rut del paciente", null=True)
    FechaHoraSolicitud = models.DateTimeField(auto_now_add=True, null=True)
    FechaAtencion = models.DateField(verbose_name="Fecha de atención", null=True)
    Estado = models.BooleanField(null=True)
    IdBloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, related_name='bloque', verbose_name="ID de bloque", null=True)
    Tarifa 	= 	models.IntegerField( null=True, default=25000)
    IdBox = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='agenda_box', null=True)
    IdContrato 	= 	models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='agenda_contrato', null=True)
    
class HistorialPago(models.Model):
	FechaHoraPago 	= 	models.DateTimeField(auto_now_add=True)
	Mes 	= 	models.IntegerField()
	Año 	= 	models.IntegerField()
	ValorPagoReal 	= 	models.DecimalField(decimal_places=2, max_digits=10)
	ValorACancelar 	= 	models.DecimalField(decimal_places=2, max_digits=10)
	EstadoPago 	= 	models.BooleanField()
	Descripcion 	= 	models.TextField(blank=True, null=True)
	FormaPago 	= 	models.IntegerField(blank=True, null=True)
	RutProfesional 	= 	models.ForeignKey(Profesionales, on_delete=models.CASCADE, related_name='historial_profesional', verbose_name="Rut del profesional")
	contrato_idcontrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
	FechaRegistro 	= 	models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del historial de pago')
	IdUsuario 	= 	models.ForeignKey(User, on_delete=models.CASCADE)