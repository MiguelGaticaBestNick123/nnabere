# Generated by Django 4.2.2 on 2023-10-23 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.CharField(max_length=100)),
                ('Estado', models.BooleanField()),
                ('HoraIni', models.TimeField()),
                ('HoraFin', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreCiudad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaContrato', models.DateField(verbose_name='Fecha del contrato')),
                ('Porcentaje', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Estado', models.BooleanField(verbose_name='Estado del contrato')),
                ('FechaIni', models.DateField(verbose_name='Fecha de inicio del contrato')),
                ('FechaFIn', models.DateField(verbose_name='Fecha de fin del contrato')),
                ('FechaRegistro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del contrato')),
                ('IdUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreEspecialidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Prevision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrePrevision', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profesionales',
            fields=[
                ('Rut', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Rut del profesional')),
                ('Nombres', models.CharField(max_length=50, verbose_name='Nombres del profesional')),
                ('ApePat', models.CharField(max_length=50, verbose_name='Apellido paterno del profesional')),
                ('ApeMat', models.CharField(max_length=50, verbose_name='Apellido materno del profesional')),
                ('Direccion', models.CharField(max_length=100, verbose_name='Dirección del profesional')),
                ('Cell', models.CharField(max_length=20, verbose_name='Número de celular del profesional')),
                ('Email', models.EmailField(max_length=254, verbose_name='Correo electrónico del profesional')),
                ('Tarifa', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tarifa por hora del profesional')),
                ('Estado', models.BooleanField(verbose_name='Estado del profesional')),
                ('FechaRegistro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del profesional')),
                ('IDEspecialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='especialidad_profesional', to='app.especialidad')),
                ('IdCiudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ciudad')),
                ('IdUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('RutPaciente', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Rut del paciente')),
                ('Nombres', models.CharField(max_length=50, verbose_name='Nombres del paciente')),
                ('ApePat', models.CharField(max_length=50, verbose_name='Apellido paterno del paciente')),
                ('ApeMat', models.CharField(max_length=50, verbose_name='Apellido materno del paciente')),
                ('OrdenAp', models.IntegerField(choices=[(1, 'Apellido Paterno'), (2, 'Apellido Materno')], verbose_name='Orden de apellidos')),
                ('FechaNac', models.DateField(verbose_name='Fecha de nacimiento del paciente')),
                ('Direccion', models.CharField(max_length=100, verbose_name='Dirección del paciente')),
                ('Cell', models.CharField(max_length=20, verbose_name='Número de celular del paciente')),
                ('Email', models.EmailField(max_length=254, verbose_name='Correo electrónico del paciente')),
                ('Estado', models.CharField(max_length=100, verbose_name='Estado del paciente')),
                ('NombreSocial', models.CharField(max_length=100, verbose_name='Nombre social del paciente')),
                ('FechaRegistro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del paciente')),
                ('IDPrevision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.prevision')),
                ('IdCiudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ciudad')),
                ('IdUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaHoraPago', models.DateTimeField(auto_now_add=True)),
                ('Mes', models.IntegerField()),
                ('Año', models.IntegerField()),
                ('ValorPagoReal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ValorACancelar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('EstadoPago', models.BooleanField()),
                ('Descripcion', models.TextField(blank=True, null=True)),
                ('FormaPago', models.IntegerField(blank=True, null=True)),
                ('FechaRegistro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro del historial de pago')),
                ('IdUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('RutProfesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_profesional', to='app.profesionales', verbose_name='Rut del profesional')),
                ('contrato_idcontrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.contrato')),
            ],
        ),
        migrations.AddField(
            model_name='contrato',
            name='RutProfesional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrato_profesional', to='app.profesionales', verbose_name='Rut del profesional'),
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Descripcion', models.TextField(blank=True, max_length=100, null=True)),
                ('ValorMensual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('FechaRegistro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro de la caja')),
                ('IdUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaHoraSolicitud', models.DateTimeField(auto_now_add=True)),
                ('FechaAtencion', models.DateField(verbose_name='Fecha de atención')),
                ('Estado', models.BooleanField()),
                ('Tarifa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('IdBloque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloque', to='app.bloque', verbose_name='ID de bloque')),
                ('IdBox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_box', to='app.box')),
                ('IdContrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_contrato', to='app.contrato')),
                ('RutPaciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paciente', to='app.pacientes', verbose_name='Rut del paciente')),
                ('RutProfesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profesional', to='app.profesionales', verbose_name='Rut del profesional')),
            ],
        ),
    ]
