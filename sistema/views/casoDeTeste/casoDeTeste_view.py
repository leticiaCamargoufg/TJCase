import os

from flask import flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from sistema import app, db, require_roles  # Importa app corretamente
from sistema.models.autenticacao.role_model import RoleModel
from sistema.models.autenticacao.usuario_model import UsuarioModel
from sistema.models.caso_teste.caso_teste_model import CasoDeTesteModel
from sistema.models.upload_arquivo.upload_arquivo_model import \
    UploadArquivoModel
from utils.utils import allowed_file



@app.route('/listarCasoDeTeste')
@require_roles
def listar_CasoDeTeste():
    casosDeTestes = CasoDeTesteModel.query.all()
    return render_template('casoDeTeste/casoDeTeste_listar.html', casosDeTestes = casosDeTestes)

@app.route('/cadastrarCasoDeTeste')
@require_roles
def caso_cadastrar():
    return render_template('')
