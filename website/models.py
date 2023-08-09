from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Patrimonio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_patrimonio = db.Column(db.String(150), unique=True)
    aquisicao = db.Column(db.Date())
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    status = db.relationship('Status')
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship('Item')
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    fabricante = db.relationship('Fabricante')
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(1000), unique=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(150), unique=True)
    servico = db.Column(db.Integer)


class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), unique=True)
    numero = db.Column(db.String(10))
    logradouro = db.Column(db.String(300))
    bairro = db.Column(db.String(300))
    cidade = db.Column(db.String(300))
    uf = db.Column(db.String(300))
    cep = db.Column(db.String(20))


class Espaco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250))
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'))
    fabricante = db.relationship('Local')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), unique=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
