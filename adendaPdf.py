import PyPDF2
#save de pdf on a variable, second prameter is for reading
#and open in binary mode
ordenCompraPdf = open('Docs/Orden_de_Compra.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(ordenCompraPdf)

print(pdfReader.numPages)

pageObj = pdfReader.getPage(0)

print(pageObj.extractText())


