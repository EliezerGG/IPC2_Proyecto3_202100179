from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET
# Create your views here.

def procesar_xml(request):
    if request.method == 'POST':
        xml_file = request.FILES.get('archivo')
        if xml_file:
            #leemos el contenido del archivo XML
            xml_content = xml_file.read().decode('utf-8')
            #parseamos el contenido del archivo XML
            root = ET.fromstring(xml_content)
            # puedes realizar operaciones con los datos del xml
            for child in root:
                print(child.tag, child.attrib)
            return HttpResponse('Archivo XML procesado')
    return HttpResponse('Error al procesar el archivo XML', status= 400)

def inicio(request):
    titulo_vista = 'Este es mi inicio'
    context = {
        "titulo": titulo_vista,
    }
    return render(request, 'inicio/inicio.html',context)

