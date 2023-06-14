from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Note, Patrimonio
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    patrimonio = Patrimonio.query.all()

    return render_template("home.html", user=current_user, patrimonio=patrimonio)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/add-ti', methods=['GET', 'POST'])
def add_ti():
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
                                        aquisicao=datetime.strptime(dataPatrimonio, '%Y-%m-%d'), tipo=tipoPatrimonio, fabricante=fabricantePatrimonio)
            db.session.add(new_patrimonio)
            db.session.commit()
            flash('Patrimonio Adicionado!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template('add_ti.html', user=current_user)
