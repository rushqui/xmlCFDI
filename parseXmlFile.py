from urllib.request import urlopen
from xml.etree import ElementTree as ET
import requests



open_url_xml = urlopen("https://storage.googleapis.com/mabe-addenda.appspot.com/FacturaTagAddenda-2019-10-16-193006.xml")
print(open_url_xml)

parser = ET.XMLParser(encoding="utf8")
xml_factura_read = ET.parse(open_url_xml, parser=parser)

print(ET.tostring(xml_factura_read.getroot()))

