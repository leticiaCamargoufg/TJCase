from sistema import app  # Agora importa `app` corretamente
from flask_login import LoginManager
from sistema.models.autenticacao.usuario_model import UsuarioModel

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return UsuarioModel.query.get(int(user_id))  # Carrega o usuário pela sessão
