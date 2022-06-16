# . du dossier website

from . import db
# Voir le document __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # importer func pour aller chercher le temps automatiquement
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Associer les notes avec un utilisateur. Avec un foreign key. Une colonne qui réfère tjrs à une colonne dans un autre base de données.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    # Clef pour identifier l'objet. Ça va prendre la primary key pour identifier l'objet uniquement et s'assurer de ne pas se tromper s'il y a des informations identiques dans la base de données.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
