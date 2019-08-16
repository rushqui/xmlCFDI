"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 15/02/2019

"""
from flask import url_for
from flask_login import UserMixin
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from run import db


class User(db.Model, UserMixin):

    __tablename__ = 'blog_user'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    numero_proveedor = db.Column(db.String(80), db.ForeignKey('proveedor.numero_proveedor', ondelete='CASCADE'), nullable=False)
    #numero_proveedor = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_numero(numero_proveedor):
       return User.query.filter_by(numero_proveedor=numero_proveedor).first()    


class Addenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(256), nullable=False)
    nombre_slug = db.Column(db.String(256), unique=True, nullable=False)
    

    def __repr__(self):
        return f'<Addenda {self.nombre}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.nombre_slug:
            self.nombre_slug = slugify(self.nombre)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.nombre_slug = f'{self.nombre_slug}-{count}'

    def public_url(self):
        return url_for('show_post', slug=self.nombre_slug)

    @staticmethod
    def get_by_slug(slug):
        return Addenda.query.filter_by(nombre_slug=slug).first()

    @staticmethod
    def get_all():
        return Addenda.query.all()


class Proveedor(db.Model, UserMixin):

    __tablename__ = 'proveedor'
    
    numero_proveedor = db.Column(db.String(80), primary_key=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    

    @staticmethod
    def get_by_numero(numero_proveedor):
       return Proveedor.query.filter_by(numero_proveedor=numero_proveedor).first()    

    @staticmethod
    def get_by_nombre(nombre):
       return Proveedor.query.filter_by(nombre=nombre).first()    