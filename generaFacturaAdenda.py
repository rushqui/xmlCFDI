from xml.etree import ElementTree as ET

ET.register_namespace('mabe', "http://recepcionfe.mabempresa.com/cfd/addenda/v1")

# namespcs =  {'factura_ns': 'http://www.sat.gob.mx/cfd/3',
#             'mabe_ns': 'http://www.mabe.com.mx'}
xmlTreeRead = ET.parse('docs/Factura.xml')

rootRead = xmlTreeRead.getroot()
print(rootRead.get('Moneda'))

# factura_raiz = root.findall('factura_ns:Comprobante', namespcs)
root = ET.Element("{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Main")
mab_factura = ET.SubElement(root,"{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Factura")
mab_factura.set('version', '1.0')
mab_factura.set('tipoDocumento', 'FACTURA')
mab_factura.set('folio', rootRead.get('Folio'))
fecha = rootRead.get('Fecha').split('T')
mab_factura.set('fecha',fecha[0])
print(fecha[0])
mab_factura.set('fecha','somefecha')


mab_moneda = ET.SubElement(mab_factura,"{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Moneda")
mab_moneda.set('tipoMoneda', rootRead.get('Moneda'))
mab_moneda.set('importeConLetra','')

mab_proveedor = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Proveedor")
mab_proveedor.set('codigo', '')

mab_entrega = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Entrega")
mab_entrega.set('plantaEntrega', '')
mab_entrega.set('calle', '')
mab_entrega.set('noExterior', '')
mab_entrega.set('codigoPostal', '')

mab_detalles = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Detalles")

consecutive = 0

for concepto in rootRead.iter('{http://www.sat.gob.mx/cfd/3}Concepto'):
    consecutive = consecutive + 1
    cantidad_str =  concepto.get('Cantidad')
    unidad_str = concepto.get('Unidad')
    importe_str = concepto.get('Importe')

    importe_flt = float(importe_str)

    print(concepto.get('Descripcion'))
    print(importe_flt)
    
    mab_detalle = ET.SubElement(mab_detalles, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Detalle")
    mab_detalle.set('noLineaArticulo', str(consecutive))
    mab_detalle.set('codigoArticulo', '')

    descripcion_product = concepto.get('Descripcion')
    mab_detalle.set('descripcion', descripcion_product)
    
    mab_detalle.set('unidad', unidad_str)
    mab_detalle.set('cantidad', cantidad_str)
    mab_detalle.set('precioSinIva', '')
    mab_detalle.set('precioConIva', '')
    mab_detalle.set('importeSinIva', '')
    mab_detalle.set('importeConIva', '')

mab_subtotal = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Subtotal")
mab_subtotal.set('importe', '')

mab_traslados = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Traslados")
mab_traslado = ET.SubElement(mab_traslados, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Traslado")
mab_traslado.set('tipo', '')
mab_traslado.set('tasa', '')
mab_traslado.set('importe', '')

mab_retenciones = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Retenciones")

mab_total = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Total")
mab_total.set('importe', '')



# root.insert(1,body)
xmlTree = ET.ElementTree(root)
xmlTree.write('docs_generados/Addenda.xml')
# ET.dump(root)




