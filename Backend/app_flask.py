from flask import Flask, jsonify, request, render_template,url_for
from flask_cors import CORS
import xml.etree.ElementTree as ET
from db import connect_to_database
from db import *
from clases import *
app = Flask(__name__)
CORS(app)

clientes = []

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
                clientes.append(cliente_nuevo)
                
                insert_cliente(nit, nombre)
            return 'Archivo XML procesado'
    return 'Error al procesar el archivo XML', 400




if __name__ == '__main__':
    app.run(debug=True, port = 5000)
    test_database_connection()