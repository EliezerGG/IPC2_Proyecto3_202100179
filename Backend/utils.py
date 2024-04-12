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
    
    
    