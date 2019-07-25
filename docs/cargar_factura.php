<?php


/* ------ SUBIMOS EL ARCHIVO XML ------- */

$allowedExts = array("xml");
$temp = explode(".", $_FILES["file"]["name"]);
$extension = end($temp);
if ((($_FILES["file"]["type"] == "text/xml"))
&& ($_FILES["file"]["size"] < 20000)
&& in_array($extension, $allowedExts))
  {
  if ($_FILES["file"]["error"] > 0)
    {
    echo "ERROR: " . $_FILES["file"]["error"] . "";
    }
  else
    {
    if (file_exists("XML/" . $_FILES["file"]["name"]))
      {
      echo $_FILES["file"]["name"] . " ya existe. ";
      }
    else
      {
      move_uploaded_file($_FILES["file"]["tmp_name"],
      "XML/" . $_FILES["file"]["name"]);
      echo "Guardado en: " . "XML/" . $_FILES["file"]["name"];
      }
    }
  }
else
  {
  echo "ERROR. El fichero debe ser XML";
  }

/* ------ LEEMOS EL XML ------- */
//$doc = new DOMDocument('1.0', 'utf-8');
$xmlfile = file_get_contents("XML/" . $_FILES["file"]["name"]);
$sxe = simplexml_load_string($xmlfile);
// Cargamos el fichero XML
//$doc->load( "XML/" . $_FILES["file"]["name"] );

//$sxe = new SimpleXMLElement(load("XML/" . $_FILES["file"]["name"] ));
// Obtenemos el nodo 

//$sxe = new SimpleXMLElement($doc); 

//$sxe = new SimpleXMLElement($xmlstr); 

$con = $sxe->getNamespaces(true);
$padre = $sxe->children($con['cfdi']);

foreach ($padre->Conceptos as $out_ns)
{   
    $ns = $out_ns->getNamespaces(true); 
    $child = $out_ns->children($ns['cfdi']);
    
    foreach ($child as $out) 
    { 
        echo $out . "<br/>";
        $atributo = $out->attributes();
        
        $ImporteConIva = $atributo->Importe;
        $PrecioConIva = $ImporteConIva +($ImporteConIva*.16);
        echo "ImporteConIva ".$PrecioConIva."<br>";
        echo "ImporteSinIva ".$atributo->Importe."<br>";
        echo "PrecioConIva ".$PrecioConIva."<br>";
        echo "PrecioSinIva ".$atributo->Importe."<br>";
        echo "Cantidad ".$atributo->Cantidad."<br>";
        echo "Unidad ".$atributo->Unidad."<br>";
        echo "Descripcion ".$atributo->Descripcion."<br>";
    }

} 


?>