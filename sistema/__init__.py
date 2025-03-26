import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import *  # Importa configurações externas
from utils.mapeamento_roles import mapeamento_roles

# Inicializa o app Flask
app = Flask(__name__)
app.secret_key = CHAVE_SECRETA_FLASK
app.config.from_object('config')

# 🔹 Configuração do diretório de uploads
UPLOAD_FOLDER = os.path.join(app.root_path, "static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório se não existir
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

# Inicializa o banco de dados
db = SQLAlchemy()
db.init_app(app)

# Instância do Migrate
migrate = Migrate(app, db)

# Instância do LoginManager
login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized():
    if request.endpoint != 'login':
        flash("Você precisa estar logado para acessar esta página!", "warning")
    return redirect(url_for('login'))

# Controle de acesso
def require_roles(f):
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        endpoint = request.endpoint
        requires_roles = mapeamento_roles.get(endpoint, [])  # Obtém a permissão necessária para a rota

        # Verifica se o usuário está autenticado
        if not current_user.is_authenticated:
            flash("Você precisa estar logado para acessar esta página!", "warning")
            return redirect(url_for("login"))

        # Obtém o cargo do usuário
        user_role = current_user.role.nome

        # Se a rota requer permissão e o usuário não tem
        if requires_roles and user_role not in requires_roles:
            flash("Você não tem permissão para acessar esta página!", "danger")
            return redirect(url_for("index"))

        return f(*args, **kwargs)

    return wrapped

# Importa os modelos
from sistema.models import base_model
from sistema.models.autenticacao import role_model, usuario_model
from sistema.models.upload_arquivo import upload_arquivo_model
from sistema.models.caso_teste import caso_teste_model
from sistema.models.projeto import projeto_model


@app.context_processor
def inject_usuario():
    """
    Torna a variável `usuario` disponível globalmente em todos os templates.
    """
    return dict(usuario=current_user)

# Importa as views
from sistema.views.autenticacao import login_view, usuario_view
from sistema.views.casoDeTeste import casoDeTeste_view
