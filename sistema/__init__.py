from functools import wraps
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_manager, current_user
from mapeamento_roles import mapeamento_roles
from config import *

app = Flask(__name__)
app.secret_key = CHAVE_SECRETA_FLASK
app.config.from_object('config')

#Inicialização do BD
db = SQLAlchemy()
db.init_app(app)

# Instância migration
migrate = Migrate(app, db)

#Instância login
login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    if request.endpoint != 'login':
        flash(('Você precisa estar logado para acessar esta página!', 'warning'))
    return redirect(url_for('login'))


#controle de acesso
def require_roles(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        endpoint = request.endpoint
        requires_roles = mapeamento_roles.get(endpoint, [])  # Obtém a permissão necessária para a rota

        # Verifica se o usuário está autenticado
        if not current_user.is_authenticated:
            flash("Você precisa estar logado para acessar esta página!", "warning")
            return redirect(url_for("login"))  # Redireciona para login se não autenticado

        # Obtém o cargo do usuário
        user_role = current_user.role.nome

        # Se a rota requer permissão e o usuário não tem
        if requires_roles and user_role not in requires_roles:
            flash("Você não tem permissão para acessar esta página!", "danger")
            return redirect(url_for("index"))  # Redireciona para home

        return f(*args, **kwargs)

    return wrapped
                                   
                                   
from sistema.models import base_model
from sistema.models.autenticacao import role_model
from sistema.models.upload_arquivo import upload_arquivo_model
from sistema.models.autenticacao import usuario_model


from sistema.views.autenticacao import login_view
from sistema.views.autenticacao import usuario_view