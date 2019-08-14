import PyPDF2
from tabula import read_pdf
 
df = read_pdf('docs/Orden_de_Compra.pdf',multiple_tables=True)
print(df)
