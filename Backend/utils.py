from babel.dates import format_date
from collections import defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from clases import meses_espanol

def respuesta_xml_config(clientes_insertados, clientes_actualizados, bancos_insertados, bancos_actualizados):
    respuesta = ET.Element("respuesta")
    
    clientes = ET.SubElement(respuesta, "clientes")
    ET.SubElement(clientes, "creados").text = str(clientes_insertados)
    ET.SubElement(clientes, "actualizados").text = str(clientes_actualizados)
    
    bancos = ET.SubElement(respuesta, "bancos")
    ET.SubElement(bancos, "creados").text = str(bancos_insertados)
    ET.SubElement(bancos, "actualizados").text = str(bancos_actualizados)
    
    xml_bytes = BytesIO()
    tree = ET.ElementTree(respuesta)
    tree.write(xml_bytes, encoding="utf-8", xml_declaration=True)
    xml_content = xml_bytes.getvalue().decode()
    
    return xml_content


def respuesta_xml_transac(facturas_insertadas, facturas_duplicadas, facturas_error, pagos_insertados, pagos_duplicados, pagos_error):
    respuesta = ET.Element("respuesta")
    
    facturas = ET.SubElement(respuesta, "facturas")
    ET.SubElement(facturas, "nuevasFacturas").text = str(facturas_insertadas)
    ET.SubElement(facturas, "facturasDuplicadas").text = str(facturas_duplicadas)
    ET.SubElement(facturas, "facturasConError").text = str(facturas_error)
    
    pagos = ET.SubElement(respuesta, "pagos")
    ET.SubElement(pagos, "nuevosPagos").text = str(pagos_insertados)
    ET.SubElement(pagos, "pagosDuplicados").text = str(pagos_duplicados)
    ET.SubElement(pagos, "pagosConError").text = str(pagos_error)
    
    xml_bytes = BytesIO()
    tree = ET.ElementTree(respuesta)
    tree.write(xml_bytes, encoding="utf-8", xml_declaration=True)
    xml_content = xml_bytes.getvalue().decode()
    
    return xml_content

def calcular_saldo(facturas, pagos):
    total_facturas = sum(float(factura['Valor']) for factura in facturas)
    total_pagos = sum(float(pago['Valor']) for pago in pagos)
    saldo = total_pagos - total_facturas
    return saldo
    
def generar_pdf(cliente_data):
    # Función para calcular el saldo del cliente
    # def calcular_saldo(facturas, pagos):
    #     total_facturas = sum(float(factura['Valor']) for factura in facturas)
    #     total_pagos = sum(float(pago['Valor']) for pago in pagos)
    #     saldo = total_pagos - total_facturas
    #     return saldo
    print(cliente_data['facturas'])
    print(cliente_data['pagos'])
    # Calcular el saldo del cliente
    saldo = calcular_saldo(cliente_data['facturas'], cliente_data['pagos'])

    # Crear un objeto BytesIO para guardar el PDF en memoria
    pdf_bytes = BytesIO()

    # Crear un nuevo documento PDF
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter)

    # Crear una lista con los datos del cliente
    datos_cliente = [
        ['NIT:', cliente_data['cliente']['NIT']],
        ['Nombre:', cliente_data['cliente']['Nombre']],
        ['Saldo:', 'Q. {:.2f}'.format(saldo)]
    ]

    # Crear una lista con los datos de las facturas y los pagos
    datos_tabla = [
        ['Fecha', 'Cargo', 'Abono']
    ]
    for factura in cliente_data['facturas']:
        datos_tabla.append([factura['Fecha'], 'Q. {:.2f}'.format(float(factura['Valor'])), ''])
    for pago in cliente_data['pagos']:
        datos_tabla.append([pago['Fecha'], '', 'Q. {:.2f}'.format(float(pago['Valor']))])

    # Crear la tabla con los datos del cliente
    tabla_cliente = Table(datos_cliente)
    tabla_cliente.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]))

    # Crear la tabla con los datos de facturas y pagos
    tabla_datos = Table(datos_tabla)
    tabla_datos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Agregar las tablas al documento
    elementos = [
        tabla_cliente,
        tabla_datos
    ]

    # Construir el PDF
    doc.build(elementos)

    # Reiniciar el cursor del objeto BytesIO a la posición inicial
    pdf_bytes.seek(0)

    return pdf_bytes




def generar_pdf_clientes(clientes_data):
    # Crear un objeto BytesIO para guardar el PDF en memoria
    pdf_bytes = BytesIO()

    # Crear un nuevo documento PDF
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter)

    # Lista para almacenar los elementos de cada cliente
    elementos_totales = []

    # Iterar sobre cada cliente en los datos de todos los clientes
    for cliente_data in clientes_data:
        # Calcular el saldo del cliente
        saldo = calcular_saldo(cliente_data['facturas'], cliente_data['pagos'])

        # Crear una lista con los datos del cliente
        datos_cliente = [
            ['NIT:', cliente_data['cliente']['NIT']],
            ['Nombre:', cliente_data['cliente']['Nombre']],
            ['Saldo:', 'Q. {:.2f}'.format(saldo)]
        ]

        # Crear una lista con los datos de las facturas y los pagos
        datos_tabla = [
            ['Fecha', 'Cargo', 'Abono']
        ]
        for factura in cliente_data['facturas']:
            datos_tabla.append([factura['Fecha'], 'Q. {:.2f}'.format(float(factura['Valor'])), ''])
        for pago in cliente_data['pagos']:
            datos_tabla.append([pago['Fecha'], '', 'Q. {:.2f}'.format(float(pago['Valor']))])

        # Crear la tabla con los datos del cliente
        tabla_cliente = Table(datos_cliente)
        tabla_cliente.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]))

        # Crear la tabla con los datos de facturas y pagos
        tabla_datos = Table(datos_tabla)
        tabla_datos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Agregar las tablas al documento
        elementos_cliente = [tabla_cliente, tabla_datos]
        elementos_totales.extend(elementos_cliente)

    # Agregar los elementos de todos los clientes al documento
    doc.build(elementos_totales)

    # Reiniciar el cursor del objeto BytesIO a la posición inicial
    pdf_bytes.seek(0)

    return pdf_bytes

def pagos_ordenados_por_mes(pagos):
    sumas_por_banco_y_mes = defaultdict(lambda: defaultdict(float))
    
    for pago in pagos:
        codigo_banco = pago['CodigoBanco']
        nombre_banco = pago['NombreBanco']
        fecha_formateada = pago['FechaFormateada']
        valor = float(pago['Valor'])
        
        fecha = datetime.strptime(fecha_formateada, '%d/%m/%Y')
        mes_anio = fecha.strftime('%B/%Y')
        
        # Traducción del nombre del mes al español
        nombre_mes_ingles = mes_anio.split('/')[0]
        nombre_mes_espanol = meses_espanol.get(nombre_mes_ingles, nombre_mes_ingles)
        
        mes_anio = nombre_mes_espanol + '/' + fecha.strftime('%Y')
        
        sumas_por_banco_y_mes[nombre_banco][mes_anio] += valor
        
    resultados = []
    
    for nombre_banco, sumas_por_mes in sumas_por_banco_y_mes.items():
        for mes_anio, suma_valor_mes in sumas_por_mes.items():
            resultado = {
                "NombreBanco": nombre_banco,
                "FechaMesAnio": mes_anio,
                "suma_valores_mes": suma_valor_mes
            }
            resultados.append(resultado)
    
    return resultados
            
