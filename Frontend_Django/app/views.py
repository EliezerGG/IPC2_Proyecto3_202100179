import requests
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def peticiones(request):
    return render(request, 'peticiones.html')


def ayuda(request):
    return render(request, 'ayuda.html')


def consultar_estado_cuenta(request):
    if request.method == 'GET':
        nit_cliente = request.GET.get('nit-cliente')

        # Realizar la solicitud al servidor Flask
        response = requests.get('http://127.0.0.1:5000/obtener-cliente', params={'nit-cliente': nit_cliente})
        print(f"Esta es la respuesta {response}")
        if response.status_code == 200:
            data = response.json()  # Convertir la respuesta JSON en un diccionario de Python
            saldo_facturas = sum([float(factura['Valor']) for factura in data['facturas']])
            saldo_pagos = sum([float(pago['Valor']) for pago in data['pagos']])
            saldo_actual = saldo_pagos - saldo_facturas
            print(f"Salgo actual {saldo_actual}")
            print(f"Esta es la data {data}")
            return render(request, 'estado_cuenta.html', {'cliente_data': data, "saldo_actual": saldo_actual})
        else:
            return HttpResponse('Error al obtener el cliente del servidor Flask', status=response.status_code)
    else:
        return HttpResponse('Método no permitido', status=405)


def consultar_estado_cuenta_clientes(request):
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:5000/obtener-clientes')

        if response.status_code == 200:
            data = response.json()
            print(f"Esta es la data de todos los clientes {data}")

            for cliente in data:
                total_facturas = sum(float(factura["Valor"]) for factura in cliente["facturas"])
                total_pagos = sum(float(pago["Valor"]) for pago in cliente["pagos"])
                saldo_actual = total_pagos - total_facturas

                cliente["saldo_actual"] = saldo_actual
            return render(request, 'estado_cuenta_clientes.html', {'clientes_data': data})
        else:
            return HttpResponse('Error al obtener los clientes del servidor Flask', status=response.status_code)
    else:
        return HttpResponse('Método no permitido', status=405)
