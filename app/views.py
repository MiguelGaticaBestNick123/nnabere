from django.shortcuts import render, redirect
from .models import Profesionales

# Create your views here.

def inicio (request):
    return render (request, 'app/home.html')

def agendar (request):
    profesional= Profesionales.objects.all()
    contexto= {
        "data":profesional
    }
    # {% for prof in data %}
    # <option value="{{ prof.Rut }}">{{ prof.Nombres }}</option>
    # {% endfor%}
    return render (request,'app/pedirhora.html', contexto)

