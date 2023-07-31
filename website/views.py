from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Patrimonio, Item, Fabricante
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    patrimonios = Patrimonio.query.all()

    return render_template("Patrimonio/home.html", user=current_user, patrimonios=patrimonios)


@views.route('/patrimonio-delete', methods=['POST'])
def patrimonio_delete():
    patrimonio = json.loads(request.data)
    patrimonioId = patrimonio['patrimonioId']
    patrimonio = Patrimonio.query.get(patrimonioId)
    if patrimonio:
        # if patrimonio.user_id == current_user.id:
        db.session.delete(patrimonio)
        db.session.commit()
    return jsonify({})


@views.route('/menu-add')
def menu_add():

    return render_template('Adicionar/menu.html', user=current_user)


@views.route('/patrimonio-add', methods=['GET', 'POST'])
def patrimonio_add():
    items = Item.query.all()
    fabricantes = Fabricante.query.all()

    if request.method == 'POST':
        numeroPatrimonio = request.form.get('numeroPatrimonio')
        dataPatrimonio = request.form.get('dataPatrimonio')
        tipoPatrimonio = request.form.get('tipoPatrimonio')
        fabricantePatrimonio = request.form.get('fabricantePatrimonio')

        patrimonio = Patrimonio.query.filter_by(
            numero_patrimonio=numeroPatrimonio).first()
        if patrimonio:
            flash('Patrimonio já registrado!', category='error')
        else:
            new_patrimonio = Patrimonio(numero_patrimonio=numeroPatrimonio,
                                        aquisicao=datetime.strptime(dataPatrimonio, '%Y-%m-%d'), item_id=tipoPatrimonio, fabricante_id=fabricantePatrimonio)
            db.session.add(new_patrimonio)
            db.session.commit()
            flash('Patrimonio Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('Adicionar/patrimonio.html', user=current_user, items=items, fabricantes=fabricantes)


@views.route('/item-add', methods=['GET', 'POST'])
def item_add():
    if request.method == 'POST':
        tipoItem = request.form.get('tipoItem')

        item = Item.query.filter_by(
            tipo=tipoItem).first()
        if item:
            flash('Item já registrado!', category='error')
        else:
            new_item = Item(tipo=tipoItem)
            db.session.add(new_item)
            db.session.commit()
            flash('Item Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('Adicionar/item.html', user=current_user)


@views.route('/fabricante_add', methods=['GET', 'POST'])
def fabricante_add():
    if request.method == 'POST':
        nomeFabricante = request.form.get('nomeFabricante')

        fabricante = Fabricante.query.filter_by(
            nome=nomeFabricante).first()
        if fabricante:
            flash('Fabricante já registrado!', category='error')
        else:
            new_fabricante = Fabricante(nome=nomeFabricante)
            db.session.add(new_fabricante)
            db.session.commit()
            flash('Item Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('Adicionar/fabricante.html', user=current_user)


@views.route('/patrimonio-info/<int:patrimonio_id>')
@login_required
def patrimonio_info(patrimonio_id):
    patrimonio = Patrimonio.query.get(patrimonio_id)

    return render_template("Patrimonio/info.html", user=current_user, patrimonio=patrimonio)


@views.route('/patrimonio-edit/<int:patrimonio_id>', methods=['GET', 'POST'])
def patrimonio_edit(patrimonio_id):
    items = Item.query.all()
    fabricantes = Fabricante.query.all()
    patrimonio = Patrimonio.query.get_or_404(patrimonio_id)

    if request.method == 'POST':
        dataPatrimonio = request.form.get('dataPatrimonio')
        tipoPatrimonio = request.form.get('tipoPatrimonio')
        fabricantePatrimonio = request.form.get('fabricantePatrimonio')

        patrimonio.aquisicao = datetime.strptime(dataPatrimonio, '%Y-%m-%d')
        patrimonio.item_id = tipoPatrimonio
        patrimonio.fabricante_id = fabricantePatrimonio

        db.session.commit()
        flash('Patrimônio editado com sucesso!', category='success')
        return redirect(url_for('views.item_info', patrimonio_id=patrimonio.id))

    return render_template('Patrimonio/edit.html', user=current_user, patrimonio=patrimonio, items=items, fabricantes=fabricantes)
