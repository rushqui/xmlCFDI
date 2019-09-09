from urllib.request import urlopen
from xml.etree import ElementTree as ET
from io import StringIO
import PyPDF2
import io
import requests
f = urlopen('https://storage.googleapis.com/mabe-addenda.appspot.com/fac-2019-09-05-234239.xml')

xmlTreeRead = ET.parse(f)

rootRead = xmlTreeRead.getroot()
print(rootRead)


#save de pdf on a variable, second parameter is for reading
#and open in binary mode
# ordenCompraPdf = open('app/static/docs/{}'.format(pdf_orden_compra),'rb')
# pdf_url = 'https://storage.cloud.google.com/mabe-addenda.appspot.com/orden-2019-09-06-053103.pdf' 
# open_pdf = urlopen(pdf_url).read()
# # memoryFile = StringIO(open_pdf)
# print(open_pdf)
# memoryFile = StringIO(open_pdf)
# read_pdf = PyPDF2.PdfFileReader(memoryFile)
# with io.BytesIO(open_pdf) as open_pdf_file:
#     read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
#     num_pages = read_pdf.getNumPages()
#     print(num_pages)

# pdfReader = PyPDF2.PdfFileReader(memoryFile)

# pageObj = pdfReader.getPage(0)
# factura_pdf_str = pageObj.extractText()

# print(factura_pdf_str)
url_str = 'https://storage.cloud.google.com/mabe-addenda.appspot.com/FacturaConAddenda617-2019-09-09-024956.xml'
list_url = url_str.split('/')
print(list_url[4])

r = requests.get('https://www.google.com/images/srpr/logo11w.png')

with open('google_logo.png', 'wb') as f:
    f.write(r.content)