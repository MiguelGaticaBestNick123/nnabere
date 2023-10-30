from django.urls import path
from .views import inicio, agendar, views


urlpatterns = [
    path('', inicio, name="inicio"),
    path ('agendar/', agendar, name="agendar"),
    path('login/', views.login_view, name='login'),

  
]    