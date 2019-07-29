import PyPDF2
#save de pdf on a variable, second prameter is for reading
#and open in binary mode
ordenCompraPdf = open('docs/Orden_de_Compra.pdf','rb')
pdfReader = PyPDF2.PdfFileReader(ordenCompraPdf)
#print(pdfReader.numPages)

pageObj = pdfReader.getPage(0)
factura_pdf_str = pageObj.extractText()

find_num_pedido = factura_pdf_str.find('Nº de pedido:') + 13
final_num_pedido = find_num_pedido + 10
#print(find_num_pedido)
print(factura_pdf_str[find_num_pedido:final_num_pedido])


