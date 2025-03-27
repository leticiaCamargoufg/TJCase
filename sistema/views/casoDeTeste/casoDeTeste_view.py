import os

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from sistema import app, db, require_roles  # Importa app corretamente
from sistema.models.autenticacao.role_model import RoleModel
from sistema.models.autenticacao.usuario_model import UsuarioModel
from sistema.models.caso_teste.caso_teste_model import CasoDeTesteModel
from sistema.models.projeto.projeto_model import ProjetoModel
from sistema.models.upload_arquivo.upload_arquivo_model import \
    UploadArquivoModel
from utils.utils import allowed_file



@app.route('/listarCasoDeTeste')
@require_roles
def listar_CasoDeTeste():
    casosDeTestes = CasoDeTesteModel.query.all()
    projetos = ProjetoModel.query.all()
    return render_template('casoDeTeste/casoDeTeste_listar.html', casosDeTestes = casosDeTestes, projetos=projetos)

@app.route('/cadastrarCasoDeTeste', methods=['GET', 'POST'])
@require_roles
def caso_cadastrar():
    if current_user.is_authenticated:
        usuario_id = current_user.id  
        
        if request.method == 'POST': 
            campo_projeto = request.form.get('campoProjeto')
            campo_status = request.form.get('campoStatus')
            campo_titulo = request.form.get('campoTitulo')
            campo_objetivo = request.form.get('campoObjetivo')
            campo_passos = request.form.get('campoPassos')
            campo_resultadoEsperado = request.form.get('campoResultadoEsperado')
            campo_observacoes = request.form.get('campoObservacoes')
        
            caso_existente = CasoDeTesteModel.query.filter_by(titulo=campo_titulo).first()
            if caso_existente:
                flash("Caso de teste já cadastrado!", "danger")
                return redirect(url_for('caso_cadastrar'))
        
            casoDeTeste = CasoDeTesteModel(
                titulo = campo_titulo,
                status=campo_status,
                objetivo=campo_objetivo,
                passos=campo_passos,
                resultado_esperado=campo_resultadoEsperado,
                observacoes=campo_observacoes,
                usuario_id=usuario_id,
                projeto_id=campo_projeto
            )
            db.session.add(casoDeTeste)
            db.session.commit()
        
            flash("Caso de Teste cadastrado com sucesso!", "success")
            return redirect(url_for('listar_CasoDeTeste'))
    return render_template('casoDeTeste/casoDeTeste_listar.html')
        



@app.route("/casoDeTeste/editar/<int:id>", methods=['GET', 'POST'])
@require_roles
def caso_editar(id):
     if current_user.is_authenticated:
        usuario_id = current_user.id  
        casoDeTeste = CasoDeTesteModel.query.filter_by(id=id).first()
    
        if not casoDeTeste:
            flash("Caso de Teste não encontrado!", "danger")
            return redirect(url_for('istar_CasoDeTeste'))  # Redireciona para a lista de usuários se não encontrar
    
        if request.method == 'POST': 
            campo_projeto = request.form.get('campoProjeto')
            campo_status = request.form.get('campoStatus')
            campo_titulo = request.form.get('campoTitulo')
            campo_objetivo = request.form.get('campoObjetivo')
            campo_passos = request.form.get('campoPassos')
            campo_resultadoEsperado = request.form.get('campoResultadoEsperado')
            campo_observacoes = request.form.get('campoObservacoes')
        
            caso_existente = CasoDeTesteModel.query.filter_by(titulo=campo_titulo).first()
            if caso_existente:
                flash("Caso de teste já cadastrado!", "danger")
                return redirect(url_for('caso_cadastrar'))

            casoDeTeste = CasoDeTesteModel(
                titulo = campo_titulo,
                status=campo_status,
                objetivo=campo_objetivo,
                passos=campo_passos,
                resultado_esperado=campo_resultadoEsperado,
                observacoes=campo_observacoes,
                usuario_id=usuario_id,
                projeto_id=campo_projeto
            )
            db.session.add(casoDeTeste)
            db.session.commit()

            flash("Caso de teste atualizado com sucesso!", "success")
            return redirect(url_for('listar_CasoDeTeste'))  # Redireciona após salvar

        return render_template('templates/casoDeTeste/casoDeTeste_editar.html')

