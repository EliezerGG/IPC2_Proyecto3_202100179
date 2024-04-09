from django.urls import path
from . import views

urlpatterns = [
    path("inicio/", views.inicio, name='inicio'),
    path("procesar-xml", views.procesar_xml, name='procesar_xml'),
]
