from flask import Flask, jsonify, request, render_template,url_for
from flask_cors import CORS
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

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