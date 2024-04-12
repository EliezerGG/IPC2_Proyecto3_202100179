import io
from flask import Flask, jsonify, request, render_template,url_for, send_file,make_response,flash,redirect
from flask_cors import CORS
import xml.etree.ElementTree as ET
from db import connect_to_database
from db import *
from clases import *
import utils
from datetime import datetime


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


@app.route('/procesar-xml', methods=['POST'])
def procesar_xml():
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
                valor = float(factura.find("valor").text)
                
                nueva_factura = Factura(numero_factura, nit_cliente, fecha, valor)
                control.facturas.append(nueva_factura)
                # print(f'Factura: {numero_factura} {nit_cliente} {fecha} {valor}')
                
                insertar_factura(numero_factura, nit_cliente, fecha, valor)
            
            for pago in root.find("pagos").findall("pago"):
                codigo_banco = pago.find("codigoBanco").text
                fecha = pago.find("fecha").text.strip()
                fecha = datetime.strptime(fecha, "%d/%m/%Y")
                nit_cliente = pago.find("NITcliente").text.strip()
                valor = float(pago.find("valor").text)
                
                nuevo_pago = Pago(codigo_banco, fecha, nit_cliente, valor)
                control.pagos.append(nuevo_pago)
                # print(f'Pago: {codigo_banco} {fecha} {nit_cliente} {valor}')
                
                insertar_pago(codigo_banco, nit_cliente, fecha, valor)  
            
            print(f"Facturas Insertadas: {control.facturas_insertadas}")
            print(f"Facturas Duplicadas: {control.facturas_duplicadas}")
            print(f"Facturas con Error: {control.facturas_error}")
            print(f"Pagos Insertados: {control.pagos_insertados}")
            print(f"Pagos con Error: {control.pagos_error}")
            
            return "Archivo XML procesado correctamente", 200
    return 'Error al procesar el archivo XML', 400


if __name__ == '__main__':
    app.run(debug=True, port = 5000)
    test_database_connection()