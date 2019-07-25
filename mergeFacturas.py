from xml.etree import ElementTree as ET

def _addenda_tag():
    ET.register_namespace('cfdi', "http://www.sat.gob.mx/cfd/3")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    xml_factura_read = ET.parse('docs/Factura.xml')
    root_factura = xml_factura_read.getroot()
    ET.SubElement(root_factura,"{http://www.sat.gob.mx/cfd/3}Addenda")
    xml_factura_read.write('docs_generados/Factura.xml')


def _merge_facturas():

    xml_factura_read = ET.parse("docs_generados/Factura.xml")
    xml_addenda = ET.parse("docs_generados/Addenda.xml")
    # xml_element_tree = None 

    # xml_element_tree = root_factura

    insertion_point = xml_factura_read.find("{http://www.sat.gob.mx/cfd/3}Addenda")
    print(insertion_point)
    print(xml_addenda.getroot())
    insertion_point.extend(xml_addenda.getroot())

    # # xml_element_tree.extend(root_addenda)
    print (insertion_point)
   
    # print(ET.tostring(xml_factura_read.getroot()))

    xml_factura_read.write('docs_generados/FacturaConAddenda.xml',encoding="utf-8",xml_declaration=True)

_addenda_tag()
_merge_facturas()






