import PyPDF2

def get_num_pedido(pdf_orden_compra):

    #save de pdf on a variable, second parameter is for reading
    #and open in binary mode
    ordenCompraPdf = open('app/static/docs/{}'.format(pdf_orden_compra),'rb')
    pdfReader = PyPDF2.PdfFileReader(ordenCompraPdf)
    
    pageObj = pdfReader.getPage(0)
    factura_pdf_str = pageObj.extractText()

    #look for the index in the extracted text from the pdf
    #plus the number of characters in the string No de pedido
    find_num_pedido = factura_pdf_str.find('Nº de pedido:') + 13

    #plus the characters size of the order number
    final_num_pedido = find_num_pedido + 10

    #get the substring for the order number
    return factura_pdf_str[find_num_pedido:final_num_pedido]


def get_num_proveedor(pdf_orden_compra):
    
    ordenCompraPdf = open('app/static/docs/{}'.format(pdf_orden_compra),'rb')
    pdfReader = PyPDF2.PdfFileReader(ordenCompraPdf)
    #print(pdfReader.numPages)

    pageObj = pdfReader.getPage(0)
    factura_pdf_str = pageObj.extractText()

    #look for the index in the extracted text from the pdf
    #plus the number of characters in the string No de pedido
    find_num_pedido = factura_pdf_str.find('CENTRO:') + 8

    #plus the characters size of the order number
    final_num_pedido = find_num_pedido + 4

    #get the substring for the order number
    return factura_pdf_str[find_num_pedido:final_num_pedido]




