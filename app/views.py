from django.shortcuts import render, redirect
from .models import Profesionales, Pacientes, Agenda, Bloque
from .forms import AgendarCitaForm
from .forms import LoginForm, CustomUserCreationForm, PacienteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
import requests
from itertools import cycle
from django.contrib.auth.decorators import permission_required, login_required



# Resto de tus importaciones y código




# Create your views here.

def inicio (request):
    return render (request, 'app/home.html')

from django.http import JsonResponse
from django.shortcuts import render, redirect



def fetch_feriados():
    # URL de la API de feriados
    api_url = 'https://api.victorsanmartin.com/feriados/en.json'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        feriados = [feriado['date'] for feriado in data.get('data', [])]
        return feriados
    except requests.exceptions.RequestException as e:
        # Manejo de errores en caso de problemas con la solicitud a la API
        print(f'Error al obtener feriados: {e}')
        return []

from django.contrib.auth.decorators import login_required

@login_required
def agendar(request):
    # Obtén el RUT del paciente que está actualmente logueado
    paciente = Pacientes.objects.get(IdUsuario=request.user)
    rut_paciente = paciente.RutPaciente
    bloques_disponibles = Bloque.objects.filter(Estado=True)


    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'reservar':
            rut_paciente = request.POST.get('rut')
            rut_profesional = request.POST.get('profesional')
            fecha = request.POST.get('fecha')
            hora = request.POST.get('hora')
            

            # Realiza la validación del RUT aquí, si es válido, continua con el proceso de reserva.
            # Si no es válido, puedes agregar un mensaje de error.

            # Luego, procede con el proceso de reserva si el RUT es válido.
            try:
                paciente = Pacientes.objects.get(RutPaciente=rut_paciente)
                profesional = Profesionales.objects.get(Rut=rut_profesional)

                # Verificar si la fecha seleccionada es un día feriado a través de la API
                feriados = fetch_feriados()

                if fecha in feriados:
                    mensaje_error = "La fecha seleccionada es un día feriado."
                    profesional = Profesionales.objects.all()
                    contexto = {"data": profesional, "error_message": mensaje_error, "rut_paciente": rut_paciente}
                    return render(request, 'app/pedirhora.html', contexto)

                agenda = Agenda(
                    RutPaciente=paciente,
                    RutProfesional=profesional,
                    FechaAtencion=fecha,
                    Tarifa=profesional.Tarifa,
                    # Agrega otros campos que necesites
                )
                agenda.save()

                return redirect('inicio')
            except Pacientes.DoesNotExist:
                # El RUT del paciente no existe en la base de datos, muestra un mensaje de error.
                mensaje_error = "El RUT del paciente no existe en la base de datos."
                profesional = Profesionales.objects.all()
                contexto = {"data": profesional, "error_message": mensaje_error, "rut_paciente": rut_paciente}
                return render(request, 'app/pedirhora.html', contexto)

    # Resto de tu vista para mostrar el formulario inicial
    profesional = Profesionales.objects.all()
    contexto = {"data": profesional, "rut_paciente": rut_paciente, "bloques": bloques_disponibles}
    return render(request, 'app/pedirhora.html', contexto)







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
    logout(request)  # Realiza la desconexión del usuario
    return render(request,'app/home.html')



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








