import io
from flask import Flask, jsonify, request, render_template,url_for, send_file,make_response,flash,redirect
from flask_cors import CORS
import xml.etree.ElementTree as ET
from db import connect_to_database
from db import *
from clases import *
import utils

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
                print(nombre, nit)
                cliente_nuevo = Cliente(nombre, nit)
                control.clientes.append(cliente_nuevo)
                
                insert_cliente(nit, nombre)
            for banco in root.find("bancos").findall("banco"):
                codigo = int(banco.find("codigo").text)
                nombre = banco.find("nombre").text
                banco_nuevo = Banco(codigo, nombre)
                control.bancos.append(banco_nuevo)
                insert_banco(codigo, nombre)
            
            print(f'Clientes Acutalizado: {control.clientes_actualizados}')
            print(f'Clientes Insertados: {control.clientes_insertados}')
            print(f'Bancos Acutalizado: {control.bancos_actualizados}')
            print(f'Bancos Insertados: {control.bancos_insertados}')
            
            
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


if __name__ == '__main__':
    app.run(debug=True, port = 5000)
    test_database_connection()