<?php
	/* Empezamos con una matriz de datos que puede proceder de cualquier fuente
	(p.e. una lectura de base de datos) */
	$matrizDeObras = array( 
		array(
			"schemaLocation"=>"http://recepcionfe.mabempresa.com/cfd/addenda/v1 http://recepcionfe.mabempresa.com/cfd/addenda/v1/mabev1.xsd", 
			"referencia1"=>"617", 
			"ordenCompra"=>"9500584281", 
			"fecha"=>"2019-06-16", 
			"folio"=>"617", 
			"tipoDocumento"=>"FACTURA", 
			"version"=>"1.0", 
			"xmlnsmabe"=>"http://recepcionfe.mabempresa.com/cfd/addenda/v1",
			"tipoMoneda"=>"MXN" ,
			"importeConLetra"=>"MIL NOVECIENTOS OCHENTA PESOS 12/100 M.N.", 
			"codigo"=>"4001065",
			"codigoPostal"=>"11210", 
			"noExterior"=>"156", 
			"calle"=>"INGENIEROS MILITARES", 
			"plantaEntrega"=>"T106",
			"importeConIva1"=>"538.24", 
			"importeConIva2"=>"34.80", 
			"importeConIva3"=>"24.36",
			"importeConIva4"=>"748.20", 
			"importeConIva5"=>"31.32", 
			"importeConIva6"=>"603.20",
			"importeSinIva1"=>"464.00", 
			"importeSinIva2"=>"30.00", 
			"importeSinIva3"=>"21.00", 
			"importeSinIva4"=>"645.00", 
			"importeSinIva5"=>"27.00", 
			"importeSinIva6"=>"520.00",
			"precioConIva1"=>"538.24", 
			"precioConIva2"=>"34.80", 
			"precioConIva3"=>"24.36", 
			"precioConIva4"=>"748.20", 
			"precioConIva5"=>"31.32",
			"precioConIva6"=>"603.20",  
			"precioSinIva1"=>"464.00", 
			"precioSinIva2"=>"30.00",
			"precioSinIva3"=>"21.00",
			"precioSinIva4"=>"645.00",
			"precioSinIva5"=>"27.00", 
			"precioSinIva6"=>"520.00", 
			"cantidad1"=>"1.0000", 
			"cantidad2"=>"1.0000",
			"cantidad3"=>"1.0000",
			"cantidad4"=>"1.0000", 
			"cantidad5"=>"1.0000", 
			"cantidad6"=>"1.0000",  
			"unidad1"=>"PIEZA",
			"unidad2"=>"PIEZA",
			"unidad3"=>"PIEZA",
			"unidad4"=>"PIEZA", 
			"unidad5"=>"PIEZA",
			"unidad6"=>"PIEZA", 
			"descripcion1"=>"SOPLETE TURNER HT-802B",
			"descripcion2"=>"DESARMADOR DE CAJA 1/4'X3'",
			"descripcion3"=>"GUANTE TIPO JAPONES",
			"descripcion4"=>"MANIFUL CON JGO DE MANGUERAS", 
			"descripcion5"=>"JGO DE PUNTAS TORX 17797",
			"descripcion6"=>"LLAVE KRAKEN PARA LAVADORAS", 
			"codigoArticulo1"=>"0", 			
			"codigoArticulo2"=>"0", 		 
			"codigoArticulo3"=>"0",
			"codigoArticulo4"=>"0", 
			"codigoArticulo5"=>"0",
			"codigoArticulo6"=>"0",
			"noLineaArticulo1"=>"1",
			"noLineaArticulo2"=>"2",
			"noLineaArticulo3"=>"3",
			"noLineaArticulo4"=>"4",
			"noLineaArticulo5"=>"5",
			"noLineaArticulo6"=>"6",
			"importe"=>"1707.00",
			"importeT"=>"273.12",
			"tasa"=>"0.16", 
			"tipo"=>"IVA",
			"importeTo"=>"1980.12"			
		)
	);

$carga_xml = simplexml_load_file( "C:/xampp/htdocs/Factura.xml");	
 //print_r($matrizDeObras);
	/* Vamos a crear un XML con XMLWriter a partir de la matriz anterior. 
	Lo vamos a crear usando programación orientada a objetos. 
	Por lo tanto, empezamos creando un objeto de la clase XMLWriter.*/
	$objetoXML = new XMLWriter();
 
	// Estructura básica del XML
	$objetoXML->openURI("addenda.xml");
	//$objetoXML->simplexml_load_file("obras2.xml");
	$objetoXML->setIndent(true);
	$objetoXML->setIndentString("\t");
	$objetoXML->startDocument('1.0', 'utf-8');

	$objetoXML->startElement("Addenda");

	foreach ($matrizDeObras as $obra){
		$objetoXML->startElement("Factura"); 
			$objetoXML->writeAttribute("xmlnsmabe", $obra["xmlnsmabe"]);
			$objetoXML->writeAttribute("version", $obra["version"]);
			$objetoXML->writeAttribute("tipoDocumento", $obra["tipoDocumento"]);
			$objetoXML->writeAttribute("folio", $obra["folio"]);
			$objetoXML->writeAttribute("fecha", $obra["fecha"]);
			$objetoXML->writeAttribute("ordenCompra", $obra["ordenCompra"]);
			$objetoXML->writeAttribute("referencia1", $obra["referencia1"]);
			$objetoXML->writeAttribute("schemaLocation", $obra["schemaLocation"]);
				$objetoXML->startElement("Moneda");
					$objetoXML->writeAttribute("tipoMoneda", $obra["tipoMoneda"]);
					$objetoXML->writeAttribute("importeConLetra", $obra["importeConLetra"]);
				$objetoXML->endElement();
				$objetoXML->startElement("Proveedor");
					$objetoXML->writeAttribute("codigo", $obra["codigo"]);
				$objetoXML->endElement();
				$objetoXML->startElement("Entrega");
					$objetoXML->writeAttribute("plantaEntrega", $obra["plantaEntrega"]);
				$objetoXML->writeAttribute("calle", $obra["calle"]);
				$objetoXML->writeAttribute("noExterior", $obra["noExterior"]);
				$objetoXML->writeAttribute("codigoPostal", $obra["codigoPostal"]);			
				$objetoXML->endElement();
				$objetoXML->startElement("Detalles");
					$objetoXML->startElement("Detalle");
						$objetoXML->writeAttribute("noLineaArticulo", $obra["noLineaArticulo1"]);
						$objetoXML->writeAttribute("codigoArticulo", $obra["codigoArticulo1"]);
						$objetoXML->writeAttribute("descripcion", $obra["descripcion1"]);
						$objetoXML->writeAttribute("unidad", $obra["unidad1"]);
						$objetoXML->writeAttribute("cantidad", $obra["cantidad1"]);
						$objetoXML->writeAttribute("precioSinIva", $obra["precioSinIva1"]);
						$objetoXML->writeAttribute("precioConIva", $obra["precioConIva1"]);
						$objetoXML->writeAttribute("importeSinIva", $obra["importeSinIva1"]);
						$objetoXML->writeAttribute("importeConIva", $obra["importeConIva1"]);
					$objetoXML->endElement();
					$objetoXML->startElement("Detalle");
						$objetoXML->writeAttribute("noLineaArticulo", $obra["noLineaArticulo2"]);
						$objetoXML->writeAttribute("codigoArticulo", $obra["codigoArticulo2"]);
						$objetoXML->writeAttribute("descripcion", $obra["descripcion2"]);
						$objetoXML->writeAttribute("unidad", $obra["unidad2"]);
						$objetoXML->writeAttribute("cantidad", $obra["cantidad2"]);
						$objetoXML->writeAttribute("precioSinIva", $obra["precioSinIva2"]);
						$objetoXML->writeAttribute("precioConIva", $obra["precioConIva2"]);
						$objetoXML->writeAttribute("importeSinIva", $obra["importeSinIva2"]);
						$objetoXML->writeAttribute("importeConIva", $obra["importeConIva2"]);
					$objetoXML->endElement();
					$objetoXML->startElement("Detalle");
						$objetoXML->writeAttribute("noLineaArticulo", $obra["noLineaArticulo3"]);
						$objetoXML->writeAttribute("codigoArticulo", $obra["codigoArticulo3"]);
						$objetoXML->writeAttribute("descripcion", $obra["descripcion3"]);
						$objetoXML->writeAttribute("unidad", $obra["unidad3"]);
						$objetoXML->writeAttribute("cantidad", $obra["cantidad3"]);
						$objetoXML->writeAttribute("precioSinIva", $obra["precioSinIva3"]);
						$objetoXML->writeAttribute("precioConIva", $obra["precioConIva3"]);
						$objetoXML->writeAttribute("importeSinIva", $obra["importeSinIva3"]);
						$objetoXML->writeAttribute("importeConIva", $obra["importeConIva3"]);
					$objetoXML->endElement();
					$objetoXML->startElement("Detalle");
						$objetoXML->writeAttribute("noLineaArticulo", $obra["noLineaArticulo4"]);
						$objetoXML->writeAttribute("codigoArticulo", $obra["codigoArticulo4"]);
						$objetoXML->writeAttribute("descripcion", $obra["descripcion4"]);
						$objetoXML->writeAttribute("unidad", $obra["unidad4"]);
						$objetoXML->writeAttribute("cantidad", $obra["cantidad4"]);
						$objetoXML->writeAttribute("precioSinIva", $obra["precioSinIva4"]);
						$objetoXML->writeAttribute("precioConIva", $obra["precioConIva4"]);
						$objetoXML->writeAttribute("importeSinIva", $obra["importeSinIva4"]);
						$objetoXML->writeAttribute("importeConIva", $obra["importeConIva4"]);
					$objetoXML->endElement();
					$objetoXML->startElement("Detalle");
						$objetoXML->writeAttribute("noLineaArticulo", $obra["noLineaArticulo5"]);
						$objetoXML->writeAttribute("codigoArticulo", $obra["codigoArticulo5"]);
						$objetoXML->writeAttribute("descripcion", $obra["descripcion5"]);
						$objetoXML->writeAttribute("unidad", $obra["unidad5"]);
						$objetoXML->writeAttribute("cantidad", $obra["cantidad5"]);
						$objetoXML->writeAttribute("precioSinIva", $obra["precioSinIva5"]);
						$objetoXML->writeAttribute("precioConIva", $obra["precioConIva5"]);
						$objetoXML->writeAttribute("importeSinIva", $obra["importeSinIva5"]);
						$objetoXML->writeAttribute("importeConIva", $obra["importeConIva5"]);
					$objetoXML->endElement();
					$objetoXML->startElement("Detalle");
						$objetoXML->writeAttribute("noLineaArticulo", $obra["noLineaArticulo6"]);
						$objetoXML->writeAttribute("codigoArticulo", $obra["codigoArticulo6"]);
						$objetoXML->writeAttribute("descripcion", $obra["descripcion6"]);
						$objetoXML->writeAttribute("unidad", $obra["unidad6"]);
						$objetoXML->writeAttribute("cantidad", $obra["cantidad6"]);
						$objetoXML->writeAttribute("precioSinIva", $obra["precioSinIva6"]);
						$objetoXML->writeAttribute("precioConIva", $obra["precioConIva6"]);
						$objetoXML->writeAttribute("importeSinIva", $obra["importeSinIva6"]);
						$objetoXML->writeAttribute("importeConIva", $obra["importeConIva6"]);
					$objetoXML->endElement();
				$objetoXML->endElement();
				$objetoXML->startElement("Subtotal");
					$objetoXML->writeAttribute("importe", $obra["importe"]);
				$objetoXML->endElement();
				$objetoXML->startElement("Traslados");
					$objetoXML->startElement("Traslado");
						$objetoXML->writeAttribute("tipo", $obra["tipo"]);
						$objetoXML->writeAttribute("tasa", $obra["tasa"]);
						$objetoXML->writeAttribute("importe", $obra["importeT"]);
					$objetoXML->endElement();
				$objetoXML->endElement();
				$objetoXML->startElement("Retenciones");
					$objetoXML->text("\n\t\t");
				$objetoXML->endElement();
				$objetoXML->startElement("Total");
					$objetoXML->writeAttribute("importe", $obra["importeTo"]);
				$objetoXML->endElement(); 
	$objetoXML->startElement('element');
  	//$objetoXML->writeAttributeNS('prefix', 'attr', 'urn:example:namespace', 'value');
  	$objetoXML->writeAttributeNs('xmlns', 'Factura', null, 'http://gegdgddcomx.org/v1/');
  	//$objetoXML->writeAttributeNs('xmlns', 'gx', null, 'http://gedcomx.org/v1/');
	$objetoXML->endElement();
	$objetoXML->startElement('response');
    $objetoXML->startElement('status');
    $objetoXML->startAttribute('code');
    $objetoXML->text('500');
    $objetoXML->endAttribute();
    $objetoXML->endElement();
	$objetoXML->endElement();
		$objetoXML->fullEndElement ();


		}

		$objetoXML->endElement(); // Final del nodo raíz, "obras"*/
	// Inicio del nodo raíz
	
	$objetoXML->endDocument(); // Final del documento


?>