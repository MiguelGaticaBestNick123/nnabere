from django.shortcuts import render, redirect
from .models import Profesionales, Pacientes, Agenda
from .forms import AgendarCitaForm

# Create your views here.

def inicio (request):
    return render (request, 'app/home.html')

def agendar (request):
    if request.method == 'POST':
        form = AgendarCitaForm(request.POST)
        if form.is_valid():
            rut_paciente = form.cleaned_data['rut']
            rut_profesional = form.cleaned_data['profesional']
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']

            paciente = Pacientes.objects.get(RutPaciente=rut_paciente)
            profesional = Profesionales.objects.get(Rut=rut_profesional)

            agenda = Agenda(
                RutPaciente=paciente,
                RutProfesional=profesional,
                FechaAtencion=fecha,
                Tarifa=profesional.Tarifa,  # Agrega la tarifa del profesional
                # Agrega otros campos que necesites
            )
            agenda.save()

            # Puedes redirigir al usuario a una página de confirmación o a donde desees
            return redirect('inicio')

    # Resto de tu vista para mostrar el formulario inicial
    profesional = Profesionales.objects.all()
    contexto = {"data": profesional}
    return render(request, 'app/pedirhora.html', contexto)







