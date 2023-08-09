from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import extract
from datetime import datetime, date
from .models import Patrimonio, Item, Fabricante, Local, Espaco, User, Status
from . import db
import json
import requests

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    patrimonios = Patrimonio.query.all()

    return render_template("Patrimonio/home.html", user=current_user, patrimonios=patrimonios)


@views.route('/locais', methods=['GET', 'POST'])
@login_required
def local():
    locais = Local.query.all()

    return render_template("Local/local.html", user=current_user, locais=locais)


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
    status = Status.query.all()
    current_date = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        numeroPatrimonio = request.form.get('numeroPatrimonio')
        dataPatrimonio = request.form.get('dataPatrimonio')
        tipoPatrimonio = request.form.get('tipoPatrimonio')
        statusPatrimonio = request.form.get('statusPatrimonio')
        fabricantePatrimonio = request.form.get('fabricantePatrimonio')

        patrimonio = Patrimonio.query.filter_by(
            numero_patrimonio=numeroPatrimonio).first()
        if patrimonio:
            flash('Patrimonio já registrado!', category='error')
        else:
            new_patrimonio = Patrimonio(numero_patrimonio=numeroPatrimonio,
                                        aquisicao=datetime.strptime(dataPatrimonio, '%Y-%m-%d'), status_id=statusPatrimonio, item_id=tipoPatrimonio, fabricante_id=fabricantePatrimonio)
            db.session.add(new_patrimonio)
            db.session.commit()
            flash('Patrimonio Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('Adicionar/patrimonio.html', user=current_user, items=items, fabricantes=fabricantes, status=status, current_date=current_date)


@views.route('/item-add', methods=['GET', 'POST'])
def item_add():
    if request.method == 'POST':
        tipoItem = request.form.get('tipoItem')
        tempoServico = request.form.get('tempoServico')

        item = Item.query.filter_by(
            tipo=tipoItem).first()
        if item:
            flash('Item já registrado!', category='error')
        else:
            new_item = Item(tipo=tipoItem, servico=tempoServico)
            db.session.add(new_item)
            db.session.commit()
            flash('Item Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('Adicionar/item.html', user=current_user)


@views.route('/fabricante-add', methods=['GET', 'POST'])
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


@views.route('/local-add', methods=['GET', 'POST'])
def local_add():
    if request.method == 'POST':
        nomeLocal = request.form.get('nomeLocal')
        cepLocal = request.form.get('cepLocal')
        logradouroLocal = request.form.get('logradouroLocal')
        bairroLocal = request.form.get('bairroLocal')
        cidadeLocal = request.form.get('cidadeLocal')
        ufLocal = request.form.get('ufLocal')
        numeroLocal = request.form.get('numeroLocal')

        local = Local.query.filter_by(
            nome=nomeLocal).first()
        if local:
            flash('Local já registrado!', category='error')
        else:
            new_local = Local(
                nome=nomeLocal, cep=cepLocal, logradouro=logradouroLocal, bairro=bairroLocal, cidade=cidadeLocal, uf=ufLocal, numero=numeroLocal)
            db.session.add(new_local)
            db.session.commit()
            flash('Local Adicionado!', category='sucess')
            return redirect(url_for('views.local'))

    return render_template('Adicionar/local.html', user=current_user)


@views.route('/consulta_cep', methods=['POST'])
def consulta_cep():
    cep = request.json.get('cep')

    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    try:
        endereco = response.json()
    except json.decoder.JSONDecodeError:
        return jsonify({'erro': 'Resposta inválida do serviço ViaCEP.'}), 500

    if response.status_code == 200 and 'erro' not in endereco:
        return jsonify(endereco)

    return jsonify({'erro': 'CEP inválido ou não encontrado.'}), 400


@views.route('/api_servico/<int:tipo_id>', methods=['POST'])
def consulta_data(tipo_id):
    ano = date.today().year
    tempo_servico = Item.query.filter_by(
        id=tipo_id).first()

    return jsonify(ano_atual=ano, tempo_servico=tempo_servico.servico)


@views.route('/patrimonio-info/<int:patrimonio_id>')
@login_required
def patrimonio_info(patrimonio_id):
    patrimonio = Patrimonio.query.get(patrimonio_id)

    return render_template("Patrimonio/info.html", user=current_user, patrimonio=patrimonio)


@views.route('/locais-info/<int:local_id>')
@login_required
def local_info(local_id):
    espacos = Espaco.query.filter_by(
        local_id=local_id)
    return render_template("Local/info.html", user=current_user, espacos=espacos)


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
        return redirect(url_for('views.patrimonio_info', patrimonio_id=patrimonio.id))

    return render_template('Patrimonio/edit.html', user=current_user, patrimonio=patrimonio, items=items, fabricantes=fabricantes)
