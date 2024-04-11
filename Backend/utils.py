import xml.etree.ElementTree as ET
from io import BytesIO

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
    