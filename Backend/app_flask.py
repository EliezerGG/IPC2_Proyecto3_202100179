from flask import Flask, jsonify, request, render_template,url_for
from flask_cors import CORS
import xml.etree.ElementTree as ET

import mysql.connector
app = Flask(__name__)
CORS(app)

def connect_to_database():
        config = {
            'user': 'root',
            'password': 'ejemplo',
            'host': 'localhost',
            'database': 'banca_virtual',
            'raise_on_warnings': True
        }

        connection = mysql.connector.connect(**config)

        return connection
    
    
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
            #leemos el contenido del archivo XML
            xml_content = xml_file.read().decode('utf-8')
            #parseamos el contenido del archivo XML
            root = ET.fromstring(xml_content)
            # puedes realizar operaciones con los datos del xml
            for child in root:
                print(child.tag, child.attrib)
                
            return 'Archivo XML procesado'
    return 'Error al procesar el archivo XML', 400




if __name__ == '__main__':
    app.run(debug=True, port = 5000)
    test_database_connection()