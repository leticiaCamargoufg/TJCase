from sistema import app, require_roles
from flask import render_template
#from flask_login import login_required


@app.route('/usuarios')
def usuarios_listar():
    return render_template('autenticacao/usuarios_listar.html')