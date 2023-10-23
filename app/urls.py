from django.urls import path
from .views import inicio, agendar


urlpatterns = [
    path('', inicio, name="inicio"),
    path ('agendar/', agendar, name="agendar"),
  
]    