from django.db import models
from django.contrib.auth.models import User

class Ciudad(models.Model):
    nombreCiudad = models.CharField(max_length=50)
class Prevision(models.Model):
    nombrePrevision = models.CharField(max_length=50)

class Especialidad(models.Model):
     nombreEspecialidad = models.CharField(max_length=50)

class Pacientes(models.Model):
    RutPaciente = models.CharField(max_length=20, verbose_name='Rut del paciente', primary_key=True, unique=True)
    Nombres = models.CharField(max_length=50, verbose_name='Nombres del paciente')
    ApePat = models.CharField(max_length=50, verbose_name='Apellido paterno del paciente')
    ApeMat = models.CharField(max_length=50, verbose_name='Apellido materno del paciente')
    OrdenAp = models.IntegerField(choices=[(1, 'Apellido Paterno'), (2, 'Apellido Materno')], verbose_name='Orden de apellidos')
    FechaNac = models.DateField(verbose_name='Fecha de nacimiento del paciente')
    Direccion = models.CharField(max_length=100, verbose_name='Dirección del paciente')
    IdCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    Cell = models.CharField(max_length=20, verbose_name='Número de celular del paciente')
    Email = models.EmailField(verbose_name='Correo electrónico del paciente')
    IDPrevision = models.ForeignKey(Prevision, on_delete=models.CASCADE)    
    Estado = models.BooleanField(verbose_name='Estado del paciente')
    NombreSocial = models.CharField(max_length=100, verbose_name='Nombre social del paciente')
    FechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del paciente')
    IdUsuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Profesionales(models.Model):
    Rut = models.CharField(max_length=20, verbose_name='Rut del profesional')
    Nombres = models.CharField(max_length=50, verbose_name='Nombres del profesional')
    ApePat = models.CharField(max_length=50, verbose_name='Apellido paterno del profesional')
    ApeMat = models.CharField(max_length=50, verbose_name='Apellido materno del profesional')
    IDEspecialidad = models.IntegerField(verbose_name='ID de la especialidad del profesional')
    Direccion = models.CharField(max_length=100, verbose_name='Dirección del profesional')
    IdCiudad = models.IntegerField(verbose_name='ID de la ciudad del profesional')
    Cell = models.CharField(max_length=20, verbose_name='Número de celular del profesional')
    Email = models.EmailField(verbose_name='Correo electrónico del profesional')
    Tarifa = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tarifa por hora del profesional')
    Estado = models.BooleanField(verbose_name='Estado del profesional')
    FechaRegistro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del profesional')
    IdUsuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Bloque(models.Model):
    Descripcion = models.CharField(max_length=100)
    Estado = models.BooleanField()
    HoraIni = models.TimeField()
    HoraFin = models.TimeField()

class Agenda(models.Model):
    RutProfesional = models.ForeignKey(Profesionales, on_delete=models.CASCADE, related_name='profesional', verbose_name="Rut del profesional")
    RutPaciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, related_name='paciente', verbose_name="Rut del paciente")
    FechaHoraSolicitud = models.DateTimeField(auto_now_add=True)
    FechaAtencion = models.DateField(verbose_name="Fecha de atención")
    Estado = models.BooleanField()
    IdBloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, related_name='bloque', verbose_name="ID de bloque")
    Tarifa 	= 	models.DecimalField(decimal_places=2, max_digits=10)
    IdBox 	= 	models.IntegerField()
    IdContrato 	= 	models.IntegerField()

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

class Box(models.Model):
	Descripcion    	=  	models.TextField(blank=True, null=True)	
	ValorMensual  	=  	models.DecimalField(decimal_places=2, max_digits=10)	
	FechaRegistro  	=  	models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro de la caja')	
	IdUsuario      	=  	models.ForeignKey(User, on_delete=models.CASCADE)

class Contrato(models.Model):
	FechaContrato  	=  	models.DateField(verbose_name='Fecha del contrato')	
	RutProfesional     	=  	models.ForeignKey(Profesionales, on_delete=models.CASCADE, verbose_name="Rut del profesional")	
	Porcentaje     	    =  	models.DecimalField(decimal_places=2, max_digits=10)
	Estado         	    =  	models.BooleanField(verbose_name='Estado del contrato')	
	FechaIni       	    =  	models.DateField(verbose_name='Fecha de inicio del contrato')	
	FechaFIn       	    =  	models.DateField(verbose_name='Fecha de fin del contrato')	
	FechaRegistro 	    =  	models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del contrato')	
	IdUsuario      	    =  	models.ForeignKey(User, on_delete=models.CASCADE)