import os
#import magic
import urllib.request
import storage
from flask import Flask, flash, request, redirect, render_template, send_from_directory, url_for, abort, current_app, send_file
from werkzeug.utils import secure_filename
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from werkzeug.exceptions import BadRequest
from xml.etree import ElementTree as ET
from forms import SignupForm, AddendaForm, LoginForm
from adendaPdf import get_num_pedido, get_num_proveedor
from mergeFacturas import _addenda_tag, _merge_facturas
from common import wahio
from app import create_app
from urllib.request import urlopen


app = create_app()

ALLOWED_EXTENSIONS = set(['pdf', 'xml'])
DIRECCION_CALLE = 'PASEO DE LAS PALAMAS'
DIRECCION_NO_EXTERIOR = '100'
DIRECCION_CP = '11000'
CODIGO_ARTICULO = '0'
UNIDAD = 'UN'
TIPO = 'IVA'
TASA = '0.16'

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

from models import User, Addenda, Proveedor

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error = error)

@app.errorhandler(500)
def server_error(error):
    return render_template("500.html", error = error)

@app.route('/error')
def generate_server_error():
    return 1/0
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
@login_required
def post_form():
    form = AddendaForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        
        post = Addenda(user_id=current_user.id, nombre=nombre)
        post.save()

    return render_template("upload.html", form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        numero_proveedor = form.numero_proveedor.data
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email o número de proveedor
        user = User.get_by_email(email)
        np = User.get_by_numero(numero_proveedor)
        no_p = Proveedor.get_by_numero(numero_proveedor)
        if not no_p:
            error = f'El número de proveedor {numero_proveedor} no está dado de alta. Favor de contactar al Administrador Atención telefónica: 55-51-96-31-68 Correo electrónico: acallejas582@gmail.com'
        elif np is not None:
            error = f'El número de proveedor {numero_proveedor} ya está siendo utilizado por otro usuario'    
        elif user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
                        
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=name, email=email, numero_proveedor=numero_proveedor)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('post_form')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post_form'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('post_form')
            return redirect(next_page)
    return render_template('login_form.html', form=form)
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



def allowed_file(filename):
    if ('.' not in filename or 
            filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS):
        raise BadRequest(
            "{0} has an invalid name or extension".format(filename))


def remove_files(folder):
    for file in os.listdir(folder):
        file_path =  os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    

# @app.route('/download/<path:filename>', methods=['GET', 'POST'])
# def download_addenda(filename):
#     return send_from_directory(directory='app/static/docs_generados/', filename=filename, as_attachment=True)


@app.route('/carga', methods=['POST'])
def upload_file():

    # if os.path.isdir('app/static/docs_generados/'):
    #     remove_files('app/static/docs_generados/')

    # remove_files('app/static/docs/')
    files_list = []

    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file : 
                allowed_file(file.filename)
                # filename = secure_filename(file.filename)
                # file.save(os.path.join('app/static/docs/', filename))
                file_url = upload_file_gs(file)
                files_list.append(file_url)
                
        flash('Archivos cargados exitosamente')

    xml_filename = generate_factura_addenda(files_list, current_user.numero_proveedor)
    url_xml_list = xml_filename.split('/')

    # storage.download_file(url_xml_list[4], url_xml_list[4])
    # return redirect(f'/download/{xml_filename}')
    return storage.download_file_from_bucket(xml_filename)
    # return redirect(xml_filename)
    # return send_file(xml_filename, as_`attachment=True)

# Upload the user-uploaded file to Google Cloud Storage
def upload_file_gs(file):

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url


@app.route('/ejecuta')
def generate_factura_addenda(files_list, num_proveedor):

    xml_factura = ''
    pdf_orden_compra = ''

    # dir_docs = 'app/static/docs_generados/'
    # try:
    #     os.mkdir(dir_docs)
    # except:
    #     print("Ya existe la carpeta 'docs_generados'")

    ET.register_namespace('mabe', "https://recepcionfe.mabempresa.com/cfd/addenda/v1")

    # namespcs =  {'factura_ns': 'http://www.sat.gob.mx/cfd/3',
    #             'mabe_ns': 'http://www.mabe.com.mx'}

    for file in files_list:
        if file.endswith('.xml'):
            xml_factura = file
        else:
            pdf_orden_compra = file

    open_urlfile = urlopen(xml_factura)

    xmlTreeRead = ET.parse(open_urlfile)

    rootRead = xmlTreeRead.getroot()
    print(rootRead.get('Moneda'))

    # factura_raiz = root.findall('factura_ns:Comprobante', namespcs)
    #root = ET.Element("{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Main")

    atrr_qname = ET.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
    root = ET.Element('Factura', {
                      atrr_qname: 'https://recepcionfe.mabempresa.com/cfd/addenda/v1 https://recepcionfe.mabempresa.com/cfd/addenda/v1/mabev1.xsd'})

    #mab_factura = ET.SubElement(root,"{http://recepcionfe.mabempresa.com/cfd/addenda/v1}Factura")

    root.set('version', '1.0')
    root.set('tipoDocumento', 'FACTURA')
    root.set('folio', rootRead.get('Folio'))
    fecha = rootRead.get('Fecha').split('T')
    root.set('fecha', fecha[0])
    num_orden_compra = get_num_pedido(pdf_orden_compra)
    root.set('ordenCompra', num_orden_compra)
    root.set('referencia1', rootRead.get('Folio'))
    root.set('xsi:xmlns','http://www.w3.org/2001/XMLSchema-instance')

    mab_moneda = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Moneda")
    mab_moneda.set('tipoMoneda', rootRead.get('Moneda'))
    total_str = rootRead.get('Total')
    split_total = total_str.split('.')
    print(split_total[0])
    total_int = int(split_total[0])
    total_dec = split_total[1]
    total_text = list(filter(None, wahio(total_int)))
    total_text_str = ' '.join(total_text).upper(
    ) + ' ' + 'PESOS' + ' ' + split_total[1] + '/100' + ' ' + 'M.N.'

    mab_moneda.set('importeConLetra', total_text_str)

    mab_proveedor = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Proveedor")
    mab_proveedor.set('codigo',  num_proveedor)

    mab_entrega = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Entrega")
    planta_entrega = get_num_proveedor(pdf_orden_compra)
    mab_entrega.set('plantaEntrega', planta_entrega)
    mab_entrega.set('calle', DIRECCION_CALLE)
    mab_entrega.set('noExterior', DIRECCION_NO_EXTERIOR)
    mab_entrega.set('codigoPostal', DIRECCION_CP)

    mab_detalles = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Detalles")

    consecutive = 0

    for concepto in rootRead.iter('{http://www.sat.gob.mx/cfd/3}Concepto'):
        consecutive = consecutive + 1
        cantidad_str = concepto.get('Cantidad')
        cantidad_flt = float(cantidad_str)
        importe_str = concepto.get('Importe')
        valor_unitario_str = concepto.get('ValorUnitario')

        importe_flt = float(importe_str)

        print(concepto.get('Descripcion'))
        print(importe_flt)

        mab_detalle = ET.SubElement(
            mab_detalles, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Detalle")
        mab_detalle.set('noLineaArticulo', str(consecutive))
        mab_detalle.set('codigoArticulo', CODIGO_ARTICULO)

        descripcion_product = concepto.get('Descripcion')
        mab_detalle.set('descripcion', descripcion_product)

        mab_detalle.set('unidad', UNIDAD)
        mab_detalle.set('cantidad', cantidad_str)
        mab_detalle.set('precioSinIva', valor_unitario_str)
        valor_unitario_flt = float(valor_unitario_str)
        valor_unitario_iva = "{0:.2f}".format(valor_unitario_flt * 1.16)
        mab_detalle.set('precioConIva', str(valor_unitario_iva))

        importe_flt = valor_unitario_flt * cantidad_flt
        importe_iva_flt = "{0:.2f}".format(importe_flt * 1.16)
        mab_detalle.set('importeSinIva', str(importe_flt))
        mab_detalle.set('importeConIva', str(importe_iva_flt))

    mab_subtotal = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Subtotal")
    subtotal = rootRead.get('SubTotal')
    mab_subtotal.set('importe', subtotal)

    mab_traslados = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Traslados")
    mab_traslado = ET.SubElement(
        mab_traslados, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Traslado")
    mab_traslado.set('tipo', TIPO)
    mab_traslado.set('tasa', TASA)
    get_traslados = rootRead.find('{http://www.sat.gob.mx/cfd/3}Impuestos')
    total_traslados = get_traslados.get('TotalImpuestosTrasladados')
    mab_traslado.set('importe', total_traslados)

    mab_retenciones = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Retenciones")

    mab_total = ET.SubElement(
        root, "{https://recepcionfe.mabempresa.com/cfd/addenda/v1}Total")

    mab_total.set('importe', total_str)

    # root.insert(1,body)
    xmlTree = ET.ElementTree(root)
    xmlTree_string = ET.tostring(xmlTree.getroot(), encoding='utf-8', method='xml')
    url_addenda_file = storage.upload_file(xmlTree_string, 'Addenda.xml', 'text/xml')
    # ET.dump(root)
    url_addendatag_file = _addenda_tag(xml_factura)
    xml_filename = _merge_facturas(rootRead.get('Folio'), url_addenda_file, url_addendatag_file)
    print(xml_filename)
    return xml_filename


