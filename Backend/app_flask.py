import io
from flask import Flask, jsonify, request, render_template,url_for, send_file,make_response,flash,redirect,Response
from flask_cors import CORS
import xml.etree.ElementTree as ET
from db import connect_to_database
from db import *
from clases import *
import utils
from datetime import datetime
import json


app = Flask(__name__)
CORS(app)
app.secret_key = "password"

@app.route("/conexion", methods=['GET'])
def test_database_connection():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] == 1:
            print('Hola')
            return "La conexión a la base de datos fue exitosa.", 200
        else:
            return "La conexión a la base de datos no fue exitosa.", 400
    except Exception as e:
        return "Ocurrió un error al intentar conectarse a la base de datos:", e
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("La conexión a la base de datos se ha cerrado.", 200)

@app.route('/limipiar-tablas', methods=['GET'])
def limpiar_tablas():
    if request.method == 'GET':
        limpiar_base_datos()
        return 'Base de Datos limpia', 200
    return 'Error al limpiar las tablas', 400



@app.route('/procesar-xml', methods=['POST'])
def procesar_xml():
    control.resetear_datos()
    if request.method == 'POST':
        xml_file = request.files.get('archivo')
        if xml_file:
            xml_content = xml_file.read().decode('utf-8')
            root = ET.fromstring(xml_content)
            for cliente in root.find("clientes").findall("cliente"):
                nit = cliente.find("NIT").text
                nit = nit.replace(" ", "")
                nombre = cliente.find("nombre").text
                cliente_nuevo = Cliente(nombre, nit)
                control.clientes.append(cliente_nuevo)
                
                insert_cliente(nit, nombre)
            for banco in root.find("bancos").findall("banco"):
                codigo = banco.find("codigo").text
                nombre = banco.find("nombre").text
                banco_nuevo = Banco(codigo, nombre)
                control.bancos.append(banco_nuevo)
                insert_banco(codigo, nombre)
            
            print(f'Clientes Acutalizado: {control.clientes_actualizados}')
            print(f'Clientes Insertados: {control.clientes_insertados}')
            print(f'Bancos Acutalizado: {control.bancos_actualizados}')
            print(f'Bancos Insertados: {control.bancos_insertados}')
            
            flash('Archivo Procesado Correctamente', 'success')
            return redirect(url_for('descargar_xml_config'))
    return 'Error al procesar el archivo XML', 400

@app.route('/descargar-xml-config')
def descargar_xml_config():
    clientes_insertados = control.clientes_insertados
    clientes_actualizados = control.clientes_actualizados
    bancos_insertados = control.bancos_insertados
    bancos_actualizados = control.bancos_actualizados
    
    xml_content = utils.respuesta_xml_config(clientes_insertados, clientes_actualizados, bancos_insertados, bancos_actualizados)
    
    # Crear una respuesta con el contenido del archivo XML
    response = make_response(xml_content)
    
    # Establecer las cabeceras para indicar que es un archivo XML para descargar
    response.headers['Content-Type'] = 'text/xml'
    response.headers['Content-Disposition'] = 'attachment; filename=respuesta.xml'

    return response

@app.route('/procesar-xml-transac', methods=['POST'])
def procesar_xml_transac():
    control.resetear_datos()
    if request.method == 'POST':
        xml_file = request.files.get('archivo')
        if xml_file:
            xml_content = xml_file.read().decode('utf-8')
            root = ET.fromstring(xml_content)
            
            for factura in root.find("facturas").findall("factura"):
                numero_factura = factura.find("numeroFactura").text.strip()
                nit_cliente = factura.find("NITcliente").text.strip()
                fecha = factura.find("fecha").text.strip()
                fecha = datetime.strptime(fecha, "%d/%m/%Y")
                fecha = fecha.strftime("%Y-%m-%d")
                valor_text = factura.find("valor").text.strip()
                
                try:
                    valor = float(valor_text)
                    if valor < 0:
                        raise ValueError(f"El valor de la factura debe ser mayor que cero. Valor ingresado: {valor}")
                except ValueError:
                    print(f"El valor '{valor_text}' no es un número flotante válido.")
                    control.facturas_error += 1
                    continue
                
                nueva_factura = Factura(numero_factura, nit_cliente, fecha, valor)
                control.facturas.append(nueva_factura)
                
                insertar_factura(numero_factura, nit_cliente, fecha, valor)

            for pago in root.find("pagos").findall("pago"):
                codigo_banco = pago.find("codigoBanco").text
                fecha = pago.find("fecha").text.strip()
                fecha = datetime.strptime(fecha, "%d/%m/%Y")
                nit_cliente = pago.find("NITcliente").text.strip()
                valor_text = pago.find("valor").text.strip()  # Corregir aquí
                
                try:
                    valor = float(valor_text)
                    if valor < 0:
                        raise ValueError(f"El valor del pago debe ser mayor que cero. Valor ingresado: {valor}")
                except ValueError:
                    print(f"El valor '{valor_text}' no es un número flotante válido.")
                    control.pagos_error += 1
                    continue
                
                nuevo_pago = Pago(codigo_banco, fecha, nit_cliente, valor)
                control.pagos.append(nuevo_pago)
                
                insertar_pago(codigo_banco, nit_cliente, fecha, valor)  
            
            print(f"Facturas Insertadas: {control.facturas_insertadas}")
            print(f"Facturas Duplicadas: {control.facturas_duplicadas}")
            print(f"Facturas con Error: {control.facturas_error}")
            print(f"Pagos Insertados: {control.pagos_insertados}")
            print(f"Pagos con Error: {control.pagos_error}")
            
            return redirect(url_for('descargar_xml_transac'))
    return 'Error al procesar el archivo XML', 400

@app.route('/descargar-xml-transac')
def descargar_xml_transac():
    facturas_insertadas = control.facturas_insertadas
    facturas_duplicadas = control.facturas_duplicadas
    facturas_error = control.facturas_error
    
    pagos_insertados = control.pagos_insertados
    pagos_duplicados = control.pagos_duplicados
    pagos_error = control.pagos_error
    
    xml_content = utils.respuesta_xml_transac(facturas_insertadas, facturas_duplicadas, facturas_error, pagos_insertados, pagos_duplicados, pagos_error)
    
    # Crear una respuesta con el contenido del archivo XML
    response = make_response(xml_content)
    
    # Establecer las cabeceras para indicar que es un archivo XML para descargar
    response.headers['Content-Type'] = 'text/xml'
    response.headers['Content-Disposition'] = 'attachment; filename=respuesta_transac.xml'

    return response

@app.route('/obtener-cliente', methods=['GET'])
def obtener_cliente():
    if request.method == 'GET':
        nit = request.args.get('nit-cliente')
        print(nit)
        cliente, facturas, pagos = obtener_info_cliente(nit)
        if cliente:
            data = jsonify(cliente= cliente, facturas=facturas, pagos=pagos)
            print("Datos del cliente:")
            print(data)
            return data, 200
    return 'Error al obtener el cliente', 400

@app.route('/descargar-pdf', methods=['GET'])
def descargar_pdf():
    if request.method == 'GET':
        nit = request.args.get('nit-cliente')
        cliente, facturas, pagos = obtener_info_cliente(nit) #dict, list, list
        
        if cliente:
            data_response = jsonify(cliente= cliente, facturas=facturas, pagos=pagos) #convertir a un diccionario
            print("HOla")
            print(data_response)
            data_dict = data_response.json #Quiero convertir a diccionario
            print(data_dict)
            print('Adios')
            pdf_bytes = utils.generar_pdf(data_dict)
        
        return send_file(
                pdf_bytes,
                mimetype='application/pdf',  # Especifica el tipo de archivo
                as_attachment=True,  # Indica que se debe descargar como archivo adjunto
                download_name='informe_cliente.pdf'  # Especifica el nombre del archivo adjunto
            )
    return 'Error al descargar el PDF', 400

@app.route('/obtener-clientes', methods=['GET'])
def obtener_clientes():
    if request.method == 'GET':
        clientes = obtener_info_todos_clientes()
        data = jsonify(clientes)
        print(data.json)
        return data, 200
    return 'Error al obtener los clientes', 400

# Retornar Clientes xml 
@app.route('/obtener-clientes-xml', methods=['GET'])
def obtener_clientes_xml():
    if request.method == 'GET':
        clientes_xml = obtener_info_todos_clientes_xml()
        if clientes_xml:
            return Response(clientes_xml, mimetype='text/xml'), 200
        else:
            return 'Error al obtener los clientes', 500
    return 'Error al obtener los clientes', 400

# -----

@app.route('/descargar-pdf-clientes', methods=['GET'])
def descargar_pdf_clientes():
    if request.method == 'GET':
        clientes = obtener_info_todos_clientes()
        data = jsonify(clientes)
        data_dict_clientes = data.json
        pdf_bytes = utils.generar_pdf_clientes(data_dict_clientes)
        print(data_dict_clientes)
        return send_file(
                pdf_bytes,
                mimetype='application/pdf',  # Especifica el tipo de archivo
                as_attachment=True,  # Indica que se debe descargar como archivo adjunto
                download_name='informe_clientes.pdf'  # Especifica el nombre del archivo adjunto
            )
    return 'Error al descargar el PDF', 400


@app.route('/obtener-pagos', methods=['GET'])
def obtener_pagos():
    if request.method == 'GET':
        pagos = obtener_todos_pagos()
        data = jsonify(pagos)
        
        data_pagos_mes = utils.pagos_ordenados_por_mes(data.json)
        data_pagos_mes_jsonify = jsonify(data_pagos_mes)
        # crear una funcion donde me sume 
        return data_pagos_mes_jsonify, 200
    return 'Error al obtener los pagos', 400

# Retornar Pagos xml
@app.route('/obtener-pagos-xml', methods=['GET'])
def obtener_pagos_xml():
    if request.method == 'GET':
        pagos_xml = obtener_todos_pagos_xml()
        if pagos_xml:
            return Response(pagos_xml, mimetype='text/xml'), 200
        else:
            return 'Error al obtener los pagos', 500
    return 'Error al obtener los pagos', 400

@app.route('/descargar-ingresos', methods=['GET'])
def descargar_ingresos():
    if request.method == 'GET':
        mes_anio = request.args.get('mes-anio')
        pagos = obtener_todos_pagos()
        data = jsonify(pagos)
        data_pagos_mes = utils.pagos_ordenados_por_mes(data.json)
        
        pdf_bytes_ingreso = utils.grafica_ingresos_por_mes(data_pagos_mes, mes_anio)
       
        return send_file(
            pdf_bytes_ingreso,
            mimetype='application/pdf',  # Especifica el tipo de archivo
            as_attachment=True,
            download_name='ingresos_mes.pdf'
        )
    return 'Error al generar el PDF', 400

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
    test_database_connection()
    
    