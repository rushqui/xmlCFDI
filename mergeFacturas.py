from xml.etree import ElementTree as ET
from flask import current_app
from urllib.request import urlopen
import storage

def _addenda_tag(xml_factura):
    ET.register_namespace('cfdi', "http://www.sat.gob.mx/cfd/3")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace('tfd', "http://www.sat.gob.mx/TimbreFiscalDigital")
    ET.register_namespace('mabe', "https://recepcionfe.mabempresa.com/cfd/addenda/v1")

    open_urlfile = urlopen(xml_factura)
    
    xml_factura_read = ET.parse(open_urlfile)

    root_factura = xml_factura_read.getroot()
    ET.SubElement(root_factura,"{http://www.sat.gob.mx/cfd/3}Addenda")
    root_factura_string = ET.tostring(root_factura, encoding='utf8', method='xml')
    url_addendatag_file = storage.upload_file(root_factura_string, 'FacturaTagAddenda.xml', 'application/xml')
    return url_addendatag_file


def _merge_facturas(folio, url_addenda_file, url_addendatag_file):

    open_url_xml = urlopen(url_addendatag_file)
    open_url_addenda = urlopen(url_addenda_file)

    xml_factura_read = ET.parse(open_url_xml)
    xml_addenda = ET.parse(open_url_addenda)

    xmlfile_name = f'FacturaConAddenda{folio}.xml'
    # xml_element_tree = None 

    # xml_element_tree = root_factura

    insertion_point = xml_factura_read.find("{http://www.sat.gob.mx/cfd/3}Addenda")
    # print(insertion_point)
    # print(xml_addenda)
    insertion_point.append(xml_addenda.getroot())

    # # xml_element_tree.extend(root_addenda)
    # print (insertion_point)
   
    xml_addenda_merged = ET.tostring(xml_factura_read.getroot(), encoding='utf8', method='xml')

    url_xmlend_file = storage.upload_file(xml_addenda_merged, xmlfile_name, 'application/xml')

    #regresa el nombre del archivo con el folio concatenado
    return url_xmlend_file




