from django import forms
from .models import Agenda, Pacientes, Profesionales
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, User

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

class CustomUserCreationForm(UserCreationForm):
    pass
    class  Meta:
        model = User
        fields = ["username", "password1","password2"]
        

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['RutPaciente', 'Nombres', 'ApePat', 'ApeMat', 'OrdenAp', 'IDPrevision', 'IdCiudad']
        labels = {
            'RutPaciente': 'Rut del paciente',
            'Nombres': 'Nombres del paciente',
            'ApePat': 'Apellido paterno del paciente',
            'ApeMat': 'Apellido materno del paciente',
            'OrdenAp': 'Orden de apellidos',
            'IDPrevision': 'Previsión',
            'IdCiudad': 'Ciudad',
        }
        widgets = {
            'RutPaciente': forms.TextInput(attrs={'class': 'form-control'}),
            'Nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'ApePat': forms.TextInput(attrs={'class': 'form-control'}),
            'ApeMat': forms.TextInput(attrs={'class': 'form-control'}),
            'OrdenAp': forms.Select(choices=[(1, 'Apellido Paterno'), (2, 'Apellido Materno')], attrs={'class': 'form-control'}),
            'IDPrevision': forms.Select(attrs={'class': 'form-control'}),
            'IdCiudad': forms.Select(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super(PacienteForm, self).__init__(*args, **kwargs)
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                self.fields['RutPaciente'].widget.attrs['readonly'] = True


