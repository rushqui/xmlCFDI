from xml.etree import ElementTree as ET
from adendaPdf import get_num_pedido
from adendaPdf import get_num_proveedor

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
num_orden_compra = get_num_pedido()
mab_factura.set('ordenCompra', num_orden_compra)
mab_factura.set('referencial','')


mab_moneda = ET.SubElement(mab_factura,"{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Moneda")
mab_moneda.set('tipoMoneda', rootRead.get('Moneda'))
mab_moneda.set('importeConLetra','')

mab_proveedor = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Proveedor")
mab_proveedor.set('codigo', '')

mab_entrega = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Entrega")
planta_entrega = get_num_proveedor()
mab_entrega.set('plantaEntrega', planta_entrega)
mab_entrega.set('calle', 'INGENIEROS MILITARES')
mab_entrega.set('noExterior', '156')
mab_entrega.set('codigoPostal', '11210')

mab_detalles = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Detalles")

consecutive = 0

for concepto in rootRead.iter('{http://www.sat.gob.mx/cfd/3}Concepto'):
    consecutive = consecutive + 1
    cantidad_str =  concepto.get('Cantidad')
    cantidad_flt = float(cantidad_str)
    importe_str = concepto.get('Importe')
    valor_unitario_str = concepto.get('ValorUnitario')

    importe_flt = float(importe_str)

    print(concepto.get('Descripcion'))
    print(importe_flt)
    
    mab_detalle = ET.SubElement(mab_detalles, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Detalle")
    mab_detalle.set('noLineaArticulo', str(consecutive))
    mab_detalle.set('codigoArticulo', '0')

    descripcion_product = concepto.get('Descripcion')
    mab_detalle.set('descripcion', descripcion_product)
    
    mab_detalle.set('unidad', 'UN')
    mab_detalle.set('cantidad', cantidad_str)
    mab_detalle.set('precioSinIva', valor_unitario_str)
    valor_unitario_flt = float(valor_unitario_str)
    valor_unitario_iva = "{0:.2f}".format(valor_unitario_flt * 1.16)
    mab_detalle.set('precioConIva', str(valor_unitario_iva))

    importe_flt = valor_unitario_flt * cantidad_flt
    importe_iva_flt = "{0:.2f}".format(importe_flt * 1.16)
    mab_detalle.set('importeSinIva', str(importe_flt))
    mab_detalle.set('importeConIva', str(importe_iva_flt))

mab_subtotal = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Subtotal")
subtotal = rootRead.get('SubTotal')
mab_subtotal.set('importe', subtotal)

mab_traslados = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Traslados")
mab_traslado = ET.SubElement(mab_traslados, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Traslado")
mab_traslado.set('tipo', 'IVA')
mab_traslado.set('tasa', '0.16')
get_traslados = rootRead.find('{http://www.sat.gob.mx/cfd/3}Impuestos')
total_traslados = get_traslados.get('TotalImpuestosTrasladados')
mab_traslado.set('importe', total_traslados)

mab_retenciones = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Retenciones")

mab_total = ET.SubElement(mab_factura, "{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Total")
total = rootRead.get('Total')
mab_total.set('importe', total)



# root.insert(1,body)
xmlTree = ET.ElementTree(root)
xmlTree.write('docs_generados/Addenda.xml')
# ET.dump(root)




