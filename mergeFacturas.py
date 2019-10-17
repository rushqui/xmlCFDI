from xml.etree import ElementTree as ET
from flask import current_app
from urllib.request import urlopen
import storage
import requests

def _addenda_tag(xml_factura):
    ET.register_namespace('cfdi', "http://www.sat.gob.mx/cfd/3")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace('tfd', "http://www.sat.gob.mx/TimbreFiscalDigital")
    ET.register_namespace('mabe', "https://recepcionfe.mabempresa.com/cfd/addenda/v1")

    open_urlfile = urlopen(xml_factura)
    
    xml_factura_read = ET.parse(open_urlfile)

    root_factura = xml_factura_read.getroot()
    ET.SubElement(root_factura,"{http://www.sat.gob.mx/cfd/3}Addenda")
    root_factura_string = ET.tostring(root_factura, encoding='utf-8', method='xml')
    url_addendatag_file = storage.upload_file(root_factura_string, 'FacturaTagAddenda.xml', 'text/xml')
    return url_addendatag_file


def _merge_facturas(folio, url_addenda_file, url_addendatag_file):

    # open_url_xml = urlopen(url_addendatag_file)
    # print("url factura original con tag de addenda: [" + url_addendatag_file + "]")
    # open_url_addenda = urlopen(url_addenda_file)
    # print("url de addenda generada: [" + url_addenda_file + "]")

    open_url_xml = requests.get(url_addendatag_file)
    open_url_xml.encoding = 'utf-8'
    print(requests.get(url_addendatag_file).encoding)
    open_url_addenda = requests.get(url_addenda_file)
    open_url_addenda.encoding = 'utf-8'
    print(requests.get(url_addenda_file).encoding)

    # parser = ET.XMLParser(encoding="utf-8")

    # xml_addenda = ET.parse(open_url_addenda, parser=parser)
    # print(ET.tostring(xml_addenda.getroot()))
    # xml_factura_read = ET.parse(open_url_xml, parser=parser)
    # print(ET.tostring(xml_factura_read.getroot()))

    xml_addenda = ET.fromstring(open_url_addenda.text)
    xml_factura_read = ET.fromstring(open_url_xml.text)


    xmlfile_name = f'FacturaConAddenda{folio}.xml'
    # xml_element_tree = None 

    # xml_element_tree = root_factura

    insertion_point = xml_factura_read.find("{http://www.sat.gob.mx/cfd/3}Addenda")
    print(insertion_point)
    print(xml_addenda)
    insertion_point.append(xml_addenda)

    # # xml_element_tree.extend(root_addenda)
    # print (insertion_point)
   
    xml_addenda_merged = ET.tostring(xml_factura_read, encoding='utf-8', method='xml')

    url_xmlend_file = storage.upload_file(xml_addenda_merged, xmlfile_name, 'text/xml')

    #regresa el nombre del archivo con el folio concatenado
    return url_xmlend_file




