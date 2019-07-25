
__facturaOriginal = None


def config():
	global __facturaOriginal
	if not __facturaOriginal:
		with open('/docs/Factura.xml',mode='r') as f:
			__config = yaml.load(f,Loader=yaml.FullLoader)
	return __config