from django import forms
from .models import Agenda, Pacientes, Profesionales

class AgendarCitaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['RutPaciente', 'RutProfesional', 'FechaAtencion', 'IdBloque']

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
