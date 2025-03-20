from sistema import app, require_roles
from flask import render_template
from sistema.models.autenticacao.role_model import RoleModel
#from flask_login import login_required


@app.route('/usuarios')
def usuarios_listar():
    return render_template('autenticacao/usuarios_listar.html')

@app.route('/cadastrar')
def usuario_cadastrar():
    cargos = RoleModel.busca_roles_asc_cargo()
    return render_template('autenticacao/usuario_cadastrar.html', cargos = cargos)