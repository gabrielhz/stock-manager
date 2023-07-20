from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Patrimonio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_patrimonio = db.Column(db.String(150), unique=True)
    aquisicao = db.Column(db.Date())
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship('Item')
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    fabricante = db.relationship('Fabricante')
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fabricante = db.Column(db.String(10000), unique=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(150), unique=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
