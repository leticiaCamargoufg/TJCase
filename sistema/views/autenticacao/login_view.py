from flask_login import login_user
from sistema import app, require_roles, request
from flask import flash, redirect, render_template, url_for

from sistema.models.autenticacao.usuario_model import *
#from flask_login import login_required

@app.route('/')
def ent():
    return render_template('autenticacao/login/login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def principal():
    return render_template('autenticacao/login/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('senha')

        usuario = UsuarioModel.query.filter_by(email=username).first()

        if not usuario:
            flash("E-mail não cadastrado!", "danger")
            return redirect(url_for('login'))

        if not check_password_hash(usuario.senha_hash, password):
            flash("Senha incorreta!", "danger")
            return redirect(url_for('login'))

        # Login bem-sucedido: registra o usuário na sessão
        login_user(usuario)

        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('index'))  # Redireciona para a página inicial

    return render_template("autenticacao/login.html")