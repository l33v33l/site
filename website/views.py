from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
# Blueprint contient plusieurs racines/url dedans et centralise ça.

views = Blueprint('views', __name__)

# Racine de la page d'accueil


@views.route('/home', methods=['GET', 'POST'])
@login_required
# Cette fonction va rouler dès que la page d'accueil va être appelée
# Alors on va "render" la page home.html quand on fait appel à /
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')

        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.commit()
            return jsonify({})
