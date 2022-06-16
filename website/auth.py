from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Fonction hash n'a pas de fonction inverse (on ne peut pas avoir la valeur avec une partie des données sauf la partie manquante. On ne peut pas avoir le mot de passe avec le hash.)

# Blueprint contient plusieurs racines/url dedans et centralise ça.

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')
            # Pour aller chercher l'information du formulaire rempli.
            # data = request.form
            # print(data)
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Le courriel est déjà utilisé par un autre compte',
                  category='error')
        elif len(email) < 4:
            flash('Le courriel doit être au moins 4 caractères', category='error')
        elif len(first_name) < 2:
            flash('Le prénom doit être au moins 2 caractère', category='error')
        elif password1 != password2:
            flash('Les deux mots de passe doivent être identiques', category='error')
        elif len(password1) < 7:
            flash('Le mot de passe doit être au moins 7 caractères', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Compte créé', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


# COmment faire pour que login et sign up puissent accepter de post request? (HTTP). Il faut rajouter une méthode dans le route comme ci-haut.

# Get request c'est quand on veut accéder à un URL

# Comment faire pour que home soit affiché quand j'appuie sur le bouton du menu home?
