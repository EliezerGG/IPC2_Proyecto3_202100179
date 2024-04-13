from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("peticiones/", views.peticiones, name="peticiones"),
    path("ayuda/", views.ayuda, name="ayuda"),
    path("consultar-estado-cuenta/", views.consultar_estado_cuenta, name="consultar-estado-cuenta"),

]
