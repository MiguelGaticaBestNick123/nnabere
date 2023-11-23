from django.shortcuts import render, redirect
from .models import Profesionales, Pacientes, Agenda, Bloque, Box, Especialidad
from .forms import AgendaForm
from .forms import LoginForm, CustomUserCreationForm, PacienteForm, ProfesionalForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
import requests
from django.views import View
from itertools import cycle
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.decorators import login_required



# Resto de tus importaciones y código




# Create your views here.

def inicio (request):
    return render (request, 'app/home.html')



def in_secretarias_group(user):
    return user.groups.filter(name='Secretarias').exists() 


def in_medicos_group(user):
    return user.groups.filter(name='Medicos').exists() 

def fetch_feriados():
    api_url = 'https://api.victorsanmartin.com/feriados/en.json'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        feriados = [feriado['date'] for feriado in data.get('data', [])]
        return feriados
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener feriados: {e}')
        return []


class AgendarView(View):
    def get(self, request):
        paciente = Pacientes.objects.get(IdUsuario=request.user)
        rut_paciente = paciente.RutPaciente
        profesionales = Profesionales.objects.all()
        form = AgendaForm()
        return render(request, 'app/pedirhora.html', {'form': form,'rut_paciente': rut_paciente, 'profesionales': profesionales})

    def post(self, request):
        form = AgendaForm(request.POST)
        print(form.errors)
        if form.is_valid():
            agenda = form.save(commit=False)
            bloque = form.cleaned_data.get('IdBloque')
            bloque.Estado = False
            bloque.save()
            agenda.save()
            return redirect('inicio')
        return render(request, 'app/pedirhora.html', {'form': form})

def fetch_bloques(request):
    rut_profesional = request.GET.get('rut_profesional')
    bloques = Bloque.objects.filter(RutProfesional=rut_profesional, Estado=True)
    bloques_list = list(bloques.values())
    profesional = Profesionales.objects.get(Rut=rut_profesional)
    tarifa = profesional.Tarifa
    data = {
        'bloques': bloques_list,
        'tarifa': tarifa,
    }
    return JsonResponse(data)

@user_passes_test(in_secretarias_group)
def secretaria(request):
    
    return render(request, 'app/secretaria.html')

@user_passes_test(in_secretarias_group)
def agendar_secretaria(request):
    paciente = Pacientes.objects.get(IdUsuario=request.user)
    rut_paciente = paciente.RutPaciente
    bloques_disponibles = Bloque.objects.filter(Estado=True)
    profesional = Profesionales.objects.all()

    if request.method == 'POST':
        print("poto")
        print(request.POST) 
        action = request.POST.get('action')
        if action == 'reservar':
            rut_paciente = request.POST.get('rut')
            rut_profesional = request.POST.get('profesional')
            fecha = request.POST.get('fecha')
            bloque_id = request.POST.get('bloque')
            tarifa = request.POST.get('tarifa') 

            try:
                paciente = Pacientes.objects.get(RutPaciente=rut_paciente)
                profesional = Profesionales.objects.get(Rut=rut_profesional)
                bloque = Bloque.objects.get(id=bloque_id)

                feriados = fetch_feriados()
                if fecha in feriados:
                    mensaje_error = "La fecha seleccionada es un día feriado."
                    contexto = {"data": profesional, "error_message": mensaje_error, "rut_paciente": rut_paciente}
                    return render(request, 'app/pedirhora.html', contexto)
                agenda = Agenda(
                    RutPaciente=paciente,
                    RutProfesional=profesional,
                    FechaAtencion=fecha,
                    Tarifa=tarifa,
                    IdBloque=bloque,
                )
                print(agenda) 
                agenda.save()
                bloque.Estado = False
                bloque.save()
                return redirect('inicio')
            except Pacientes.DoesNotExist:
                mensaje_error = "El RUT del paciente no existe en la base de datos."
                contexto = {"data": profesional, "error_message": mensaje_error, "rut_paciente": rut_paciente}
                return render(request, 'app/pedirhora.html', contexto)
            except Exception as e:
                print(e)
                mensaje_error = "Ocurrió un error al guardar la agenda."
                contexto = {"data": profesional, "error_message": mensaje_error, "rut_paciente": rut_paciente}
                return render(request, 'app/agendar_secretaria.html', contexto)
    print("test")
    contexto = {"data": profesional, "rut_paciente": rut_paciente, "bloques": bloques_disponibles}
    return render(request, 'app/agendar_secretaria.html', contexto)



def login_view(request):
    mensaje = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        else:
            mensaje = "Mal ahí, no se pudo autenticar"
    else:
        form = LoginForm(request)
    contexto = {
        "form": form,
        "mensaje": mensaje
    }
    return render(request, 'app/login.html', contexto)



def logout_view(request):
    logout(request)  
    return render(request,'app/home.html')

def eliminar_reserva(request, reserva_id):
    reserva = Agenda.objects.get(id=reserva_id)
    Bloque.objects.filter(id=reserva.IdBloque.id).update(Estado=True)
    reserva.delete()

    return redirect('reservas')

def contacto(request):
    return render(request, 'app/contacto.html')

@login_required
def reservas(request):
    paciente = Pacientes.objects.get(IdUsuario=request.user)
    reservas = Agenda.objects.filter(RutPaciente=paciente.RutPaciente)
    contexto = {"reservas": reservas}
    return render(request,'app/reservas.html', contexto)


def verificar_rut(request):
    rut = request.GET.get('rut')
    try:
        paciente = Pacientes.objects.get(RutPaciente=rut)
        existe = True
    except Pacientes.DoesNotExist:
        existe = False

    return JsonResponse({'existe': existe})

def registro(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario = CustomUserCreationForm(data=request.POST)
            formulario.save()
            User = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, User)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="datosform")
    data = {
    'form': CustomUserCreationForm()
        }
    return render(request, 'app/registro.html', data)
def validar_rut(rut):
    rut = rut.upper()
    rut = rut.replace("-","")
    rut = rut.replace(".","")
    aux = rut[:-1]
    dv = rut[-1:]
 
    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido,factors))
    res = (-s)%11
 
    if str(res) == dv:
        return True
    elif dv=="K" and res==10:
        return True
    else:
        return False
@login_required
def datosform(request):
    try:
        paciente = Pacientes.objects.get(IdUsuario=request.user)
    except Pacientes.DoesNotExist:
        paciente = None

    if request.method == 'POST':
        post = request.POST.copy()  # Hacer una copia mutable del objeto POST
        if paciente is not None:
            post['RutPaciente'] = paciente.RutPaciente  # Sobrescribir el RutPaciente con el valor existente
        form = PacienteForm(post, instance=paciente)  # Pasar el objeto POST modificado al formulario
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.IdUsuario = request.user
            paciente.save()
            return redirect('inicio')
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'app/registro2.html', {'form': form})

@user_passes_test(in_secretarias_group)
def lista_medico(request):
    medicos = Profesionales.objects.all()
    return render(request, 'app/lista_medico.html', {'medicos': medicos})


@user_passes_test(in_secretarias_group)
def lista_reserva(request):
    reservas = Agenda.objects.all()
    return render(request, 'app/lista_reserva.html', {'reservas': reservas})


@user_passes_test(in_medicos_group)
def lista_paciente(request):
    usuario_actual = request.user
    agendas = Agenda.objects.filter(RutProfesional__IdUsuario=usuario_actual)
    pacientes = [agenda.RutPaciente for agenda in agendas]
    return render(request, 'app/lista_paciente.html', {'pacientes': pacientes})

@user_passes_test(in_medicos_group)
def datosform_medico(request):
    try:
        profesional = Profesionales.objects.get(IdUsuario=request.user)
    except Profesionales.DoesNotExist:
        profesional = None

    if request.method == 'POST':
        post = request.POST.copy()  # Hacer una copia mutable del objeto POST
        if profesional is not None:
            post['Rut'] = profesional.Rut  # Sobrescribir el Rut con el valor existente
        form = ProfesionalForm(post, instance=profesional)  # Pasar el objeto POST modificado al formulario
        if form.is_valid():
            profesional = form.save(commit=False)
            profesional.IdUsuario = request.user
            profesional.save()
            return redirect('inicio')
    else:
        form = ProfesionalForm(instance=profesional)

    return render(request, 'app/datosform_medico.html', {'form': form, 'profesional': profesional})
