from sistema import app, require_roles
from flask import render_template
#from flask_login import login_required


@app.route('/')
def principal():
    return render_template('estrutura/dashboard.html')