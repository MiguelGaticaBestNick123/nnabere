from django import forms
from .models import Agenda, Pacientes, Profesionales
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    pass

class AgendarCitaForm(forms.Form):
    rut = forms.CharField(label='RUT del Paciente', max_length=20)
    profesional = forms.CharField(label='Profesional', max_length=20)
    fecha = forms.DateField(label='Fecha de atención')
    hora = forms.TimeField(label='Hora de atención')

class BuscarCitasForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    profesional = forms.ModelChoiceField(queryset=Profesionales.objects.all())

class RegistrarPacienteForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = '__all__'  # Puedes personalizar los campos aquí

class RegistrarMedicoForm(forms.ModelForm):
    class Meta:
        model = Profesionales
        fields = '__all__'  # Puedes personalizar los campos aquí

