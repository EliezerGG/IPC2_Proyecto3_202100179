from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("peticiones/", views.peticiones, name="peticiones"),
    path("ayuda/", views.ayuda, name="ayuda"),
    path("consultar-estado-cuenta/", views.consultar_estado_cuenta, name="consultar-estado-cuenta"),
    path("consultar-estado-cuenta-clientes/", views.consultar_estado_cuenta_clientes, name="consultar-estado-cuenta-clientes"),

]
