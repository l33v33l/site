# https://www.youtube.com/watch?v=dam0GPOAvVI&t=1472s
# Install PIP mac : https://www.geeksforgeeks.org/how-to-install-pip-in-macos/

# https://stackoverflow.com/questions/57150052/why-does-this-output-appear-after-typing-python3-v-in-terminal

"""
https://www.geeksforgeeks.org/how-to-install-pip-in-macos/
python3 install pip 
pip install flask
pip install flask-login  
pip install flask-sqlalchemy

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # __name__ = le nom du fichier
    app = Flask(__name__)
    # Variable d'environnement qui permet d'encrypter les cookies et data de session
    # SECRET_KEY doit vraiment être écrit avec des lettres majuscules. Sinon, ça ne fonctionne pas!!!
    app.config['SECRET_KEY'] = 'dsadadwsd312'
    # f' pour utiliser les {} pour le code python
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Ça dit qu'on va utiliser cette app avec la base de données.
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Ça dit de loader comme un user
    @login_manager.user_loader
    def load_user(id):
        # Comme filter by mais va chercher pour l'ID
        return User.query.get(int(id))

    return app

# Ça vérifie si la base de donnée est déjà créée


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database! ')
