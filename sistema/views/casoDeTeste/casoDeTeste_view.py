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
def caso_listar():
    casosDeTestes = CasoDeTesteModel.query.filter_by(ativo=1).all()
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
            return redirect(url_for('caso_listar'))
    return render_template('casoDeTeste/casoDeTeste_listar.html')
        



@app.route("/casoDeTeste/editar/<int:id>", methods=['GET', 'POST'])
@require_roles
def caso_editar(id):
    projetos = ProjetoModel.query.all()
    
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar esta página.", "danger")
        return redirect(url_for('login'))  # Redireciona se não estiver autenticado

    usuario_id = current_user.id  
    casoDeTeste = CasoDeTesteModel.query.get(id)

    if not casoDeTeste:
        flash("Caso de Teste não encontrado!", "danger")
        return redirect(url_for('caso_listar'))  

    if request.method == 'POST': 
        campo_projeto = request.form.get('campoProjeto')
        campo_status = request.form.get('campoStatus')
        campo_titulo = request.form.get('campoTitulo')
        campo_objetivo = request.form.get('campoObjetivo')
        campo_passos = request.form.get('campoPassos')
        campo_resultadoEsperado = request.form.get('campoResultadoEsperado')
        campo_observacoes = request.form.get('campoObservacoes')

        # Verifica se já existe um caso de teste com o mesmo título (exceto o atual)
        caso_existente = CasoDeTesteModel.query.filter(
            CasoDeTesteModel.titulo == campo_titulo, CasoDeTesteModel.id != id
        ).first()

        if caso_existente:
            flash("Já existe um caso de teste com este título!", "danger")
            return redirect(url_for('caso_editar', id=id))

        # Atualiza os dados do caso de teste existente
        casoDeTeste.titulo = campo_titulo
        casoDeTeste.status = campo_status
        casoDeTeste.objetivo = campo_objetivo
        casoDeTeste.passos = campo_passos
        casoDeTeste.resultado_esperado = campo_resultadoEsperado
        casoDeTeste.observacoes = campo_observacoes
        casoDeTeste.usuario_id = usuario_id
        casoDeTeste.projeto_id = campo_projeto

        db.session.commit()

        flash("Caso de teste atualizado com sucesso!", "success")
        return redirect(url_for('caso_listar'))

    return render_template('casoDeTeste/casoDeTeste_editar.html', caso=casoDeTeste, projetos = projetos)


@app.route("/casoDeTeste/excluir/<int:id>", methods=['GET', 'POST'])
@require_roles
def caso_excluir(id):
    casoDeTeste = CasoDeTesteModel.query.get(id)

    if not casoDeTeste:
        flash("Caso de Teste não encontrado!", "danger")
        return redirect(url_for("caso_listar"))

    casoDeTeste.ativo = 0
    casoDeTeste.deletado = 1
    db.session.commit()  # Salva a alteração no banco

    flash("Caso de teste excluído com sucesso!", "success")
    casosDeTestes = CasoDeTesteModel.query.all()
    return redirect(url_for('caso_listar', casosDeTestes = casosDeTestes))
