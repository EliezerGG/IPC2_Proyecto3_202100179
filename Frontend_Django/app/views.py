from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def peticiones(request):
    return render(request, 'peticiones.html')


def ayuda(request):
    return render(request, 'ayuda.html')

# --- pruebas

